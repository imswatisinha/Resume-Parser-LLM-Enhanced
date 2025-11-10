"""
RAG (Retrieval Augmented Generation) Service
Handles vector storage, similarity search, and retrieval operations.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import hashlib
from datetime import datetime, timedelta
import json

from config.settings import get_config
from core.exceptions import ExternalAPIError, ValidationError, handle_errors
from core.logging_system import get_logger, log_performance, log_function_calls
from core.security import get_security_manager

logger = get_logger(__name__)

class RAGService:
    """Service for retrieval augmented generation operations."""
    
    def __init__(self):
        self.config = get_config()
        self.security = get_security_manager()
        self.embedding_model = None
        self._model_name = "all-MiniLM-L6-v2"
        self._pinecone_client = None
        self._index = None
        self._embedding_cache = {}
        self._cache_max_size = 1000
        
        # Statistics
        self._stats = {
            "embeddings_generated": 0,
            "similarity_searches": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "pinecone_operations": 0
        }
        
        logger.info("RAG service initialized")
    
    def _initialize_embedding_model(self):
        """Lazy initialization of embedding model."""
        if self.embedding_model is None:
            try:
                logger.info(f"Loading embedding model: {self._model_name}")
                self.embedding_model = SentenceTransformer(self._model_name)
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {str(e)}")
                raise ExternalAPIError("SentenceTransformer", None, f"Model loading failed: {str(e)}")
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client and index."""
        if self._pinecone_client is None and self.config.pinecone.enabled:
            try:
                import pinecone
                
                # Get API key securely
                api_key = self.security.get_api_key('PINECONE_API_KEY')
                if not api_key:
                    logger.warning("Pinecone API key not found, disabling Pinecone functionality")
                    return False
                
                # Initialize Pinecone
                pinecone.init(
                    api_key=api_key,
                    environment=self.config.pinecone.environment
                )
                
                # Connect to index
                if self.config.pinecone.index_name in pinecone.list_indexes():
                    self._index = pinecone.Index(self.config.pinecone.index_name)
                    logger.info(f"Connected to Pinecone index: {self.config.pinecone.index_name}")
                    return True
                else:
                    logger.warning(f"Pinecone index '{self.config.pinecone.index_name}' not found")
                    return False
                    
            except ImportError:
                logger.warning("Pinecone library not installed, disabling Pinecone functionality")
                return False
            except Exception as e:
                logger.error(f"Failed to initialize Pinecone: {str(e)}")
                return False
        
        return self._index is not None
    
    @log_function_calls(include_args=False)
    @log_performance(threshold_seconds=5.0)
    def generate_embedding(self, text: str, cache_key: str = None) -> np.ndarray:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            cache_key: Optional cache key for reusing embeddings
            
        Returns:
            Embedding vector as numpy array
        """
        if not text or not text.strip():
            raise ValidationError("Empty text provided for embedding generation")
        
        # Check cache first
        if cache_key:
            cached_embedding = self._get_cached_embedding(cache_key)
            if cached_embedding is not None:
                self._stats["cache_hits"] += 1
                return cached_embedding
            self._stats["cache_misses"] += 1
        
        # Initialize model if needed
        self._initialize_embedding_model()
        
        try:
            # Generate embedding
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            
            # Cache the result
            if cache_key:
                self._cache_embedding(cache_key, embedding)
            
            self._stats["embeddings_generated"] += 1
            
            logger.debug(f"Generated embedding: shape={embedding.shape}, norm={np.linalg.norm(embedding):.3f}")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise ExternalAPIError("SentenceTransformer", None, f"Embedding generation failed: {str(e)}")
    
    def _get_cached_embedding(self, cache_key: str) -> Optional[np.ndarray]:
        """Get embedding from cache."""
        cache_entry = self._embedding_cache.get(cache_key)
        if cache_entry:
            # Check if cache entry is still valid (1 hour TTL)
            if datetime.now() - cache_entry['timestamp'] < timedelta(hours=1):
                return cache_entry['embedding']
            else:
                # Remove expired entry
                del self._embedding_cache[cache_key]
        return None
    
    def _cache_embedding(self, cache_key: str, embedding: np.ndarray):
        """Cache embedding with TTL."""
        # Remove oldest entries if cache is full
        if len(self._embedding_cache) >= self._cache_max_size:
            oldest_key = min(self._embedding_cache.keys(), 
                           key=lambda k: self._embedding_cache[k]['timestamp'])
            del self._embedding_cache[oldest_key]
        
        self._embedding_cache[cache_key] = {
            'embedding': embedding,
            'timestamp': datetime.now()
        }
    
    @log_function_calls(include_args=False)
    @log_performance(threshold_seconds=10.0)
    def store_document_embedding(
        self, 
        document_id: str,
        text: str,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        Store document embedding in vector database.
        
        Args:
            document_id: Unique document identifier
            text: Document text to embed
            metadata: Additional metadata to store
            
        Returns:
            Success status
        """
        if not self._initialize_pinecone():
            logger.warning("Pinecone not available, skipping vector storage")
            return False
        
        try:
            # Generate embedding
            cache_key = f"doc_{hashlib.md5(text.encode()).hexdigest()}"
            embedding = self.generate_embedding(text, cache_key)
            
            # Prepare metadata
            store_metadata = {
                'text_preview': text[:500],  # Store preview for debugging
                'text_length': len(text),
                'timestamp': datetime.now().isoformat(),
                'document_type': 'resume'
            }
            
            if metadata:
                store_metadata.update(metadata)
            
            # Store in Pinecone
            self._index.upsert([{
                'id': document_id,
                'values': embedding.tolist(),
                'metadata': store_metadata
            }])
            
            self._stats["pinecone_operations"] += 1
            
            logger.info(f"Stored document embedding: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store document embedding: {str(e)}")
            return False
    
    @log_function_calls(include_args=False)
    @log_performance(threshold_seconds=10.0)
    def find_similar_documents(
        self,
        query_text: str,
        top_k: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Find similar documents using vector similarity search.
        
        Args:
            query_text: Text to search for
            top_k: Number of results to return
            score_threshold: Minimum similarity score
            
        Returns:
            List of similar documents with metadata
        """
        if not self._initialize_pinecone():
            logger.warning("Pinecone not available, returning empty results")
            return []
        
        try:
            # Generate query embedding
            cache_key = f"query_{hashlib.md5(query_text.encode()).hexdigest()}"
            query_embedding = self.generate_embedding(query_text, cache_key)
            
            # Search in Pinecone
            results = self._index.query(
                vector=query_embedding.tolist(),
                top_k=top_k,
                include_metadata=True,
                include_values=False
            )
            
            # Filter and format results
            similar_docs = []
            for match in results.matches:
                if match.score >= score_threshold:
                    similar_docs.append({
                        'id': match.id,
                        'score': float(match.score),
                        'metadata': match.metadata,
                        'relevance': self._calculate_relevance_score(match.score, match.metadata)
                    })
            
            self._stats["similarity_searches"] += 1
            self._stats["pinecone_operations"] += 1
            
            logger.info(f"Found {len(similar_docs)} similar documents (threshold: {score_threshold})")
            
            return similar_docs
            
        except Exception as e:
            logger.error(f"Similarity search failed: {str(e)}")
            return []
    
    def _calculate_relevance_score(self, similarity_score: float, metadata: Dict[str, Any]) -> float:
        """Calculate comprehensive relevance score."""
        relevance = similarity_score
        
        # Boost recent documents
        if 'timestamp' in metadata:
            try:
                doc_date = datetime.fromisoformat(metadata['timestamp'])
                days_old = (datetime.now() - doc_date).days
                recency_boost = max(0, (30 - days_old) / 30) * 0.1  # Up to 10% boost for recent docs
                relevance += recency_boost
            except:
                pass
        
        # Boost documents with more content
        if 'text_length' in metadata:
            length = metadata['text_length']
            if length > 1000:  # Substantial content
                relevance += 0.05
        
        return min(relevance, 1.0)  # Cap at 1.0
    
    def batch_generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts efficiently."""
        if not texts:
            return []
        
        self._initialize_embedding_model()
        
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True, batch_size=32)
            self._stats["embeddings_generated"] += len(texts)
            
            logger.info(f"Generated {len(embeddings)} embeddings in batch")
            return embeddings
            
        except Exception as e:
            logger.error(f"Batch embedding generation failed: {str(e)}")
            raise ExternalAPIError("SentenceTransformer", None, f"Batch embedding failed: {str(e)}")
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        if not text1 or not text2:
            return 0.0
        
        try:
            # Generate embeddings
            embeddings = self.batch_generate_embeddings([text1, text2])
            
            # Calculate cosine similarity
            embedding1, embedding2 = embeddings[0], embeddings[1]
            
            # Normalize vectors
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {str(e)}")
            return 0.0
    
    def get_document_clusters(self, embeddings: List[np.ndarray], n_clusters: int = 5) -> List[int]:
        """Cluster documents based on embeddings."""
        if len(embeddings) < n_clusters:
            return list(range(len(embeddings)))
        
        try:
            from sklearn.cluster import KMeans
            
            # Convert to array
            embedding_matrix = np.array(embeddings)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(embedding_matrix)
            
            logger.info(f"Clustered {len(embeddings)} documents into {n_clusters} groups")
            
            return cluster_labels.tolist()
            
        except ImportError:
            logger.warning("scikit-learn not available, skipping clustering")
            return list(range(len(embeddings)))
        except Exception as e:
            logger.error(f"Clustering failed: {str(e)}")
            return list(range(len(embeddings)))
    
    def delete_document(self, document_id: str) -> bool:
        """Delete document from vector store."""
        if not self._initialize_pinecone():
            return False
        
        try:
            self._index.delete(ids=[document_id])
            self._stats["pinecone_operations"] += 1
            
            logger.info(f"Deleted document: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {str(e)}")
            return False
    
    def get_index_statistics(self) -> Dict[str, Any]:
        """Get vector index statistics."""
        if not self._initialize_pinecone():
            return {"available": False, "reason": "Pinecone not initialized"}
        
        try:
            stats = self._index.describe_index_stats()
            
            return {
                "available": True,
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": len(stats.namespaces) if stats.namespaces else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get index statistics: {str(e)}")
            return {"available": False, "error": str(e)}
    
    def clear_cache(self):
        """Clear embedding cache."""
        cleared_count = len(self._embedding_cache)
        self._embedding_cache.clear()
        logger.info(f"Cleared {cleared_count} cached embeddings")
    
    def get_service_statistics(self) -> Dict[str, Any]:
        """Get service statistics."""
        cache_hit_rate = 0.0
        total_requests = self._stats["cache_hits"] + self._stats["cache_misses"]
        if total_requests > 0:
            cache_hit_rate = self._stats["cache_hits"] / total_requests
        
        return {
            **self._stats,
            "cache_hit_rate": cache_hit_rate,
            "cache_size": len(self._embedding_cache),
            "model_loaded": self.embedding_model is not None,
            "pinecone_connected": self._index is not None
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check of RAG service."""
        health_status = {
            "healthy": True,
            "components": {}
        }
        
        try:
            # Test embedding model
            self._initialize_embedding_model()
            test_embedding = self.generate_embedding("test text")
            health_status["components"]["embedding_model"] = {
                "status": "healthy",
                "model": self._model_name,
                "embedding_dimension": len(test_embedding)
            }
            
        except Exception as e:
            health_status["healthy"] = False
            health_status["components"]["embedding_model"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Test Pinecone connection
        if self.config.pinecone.enabled:
            try:
                pinecone_healthy = self._initialize_pinecone()
                if pinecone_healthy:
                    index_stats = self.get_index_statistics()
                    health_status["components"]["pinecone"] = {
                        "status": "healthy",
                        "index_stats": index_stats
                    }
                else:
                    health_status["components"]["pinecone"] = {
                        "status": "unavailable",
                        "reason": "Failed to initialize"
                    }
            except Exception as e:
                health_status["components"]["pinecone"] = {
                    "status": "error",
                    "error": str(e)
                }
        else:
            health_status["components"]["pinecone"] = {
                "status": "disabled",
                "reason": "Pinecone disabled in configuration"
            }
        
        # Add service statistics
        health_status["service_stats"] = self.get_service_statistics()
        
        return health_status

# Global service instance
_rag_service: Optional[RAGService] = None

def get_rag_service() -> RAGService:
    """Get the global RAG service."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service