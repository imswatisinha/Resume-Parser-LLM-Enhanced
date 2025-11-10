"""
Streamlined Resume Parser Application
Modern architecture with separated services and clean interfaces.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import get_config
from core.logging_system import get_logger
from ui.ui_service import get_ui_service
from services.orchestrator import get_orchestrator, process_resume_file

# Initialize services
logger = get_logger(__name__)

def main():
    """Main application entry point."""
    try:
        # Initialize configuration and services
        config = get_config()
        ui_service = get_ui_service()
        orchestrator = get_orchestrator()
        
        # Setup Streamlit page
        ui_service.setup_page_config()
        
        # Render header
        ui_service.render_header()
        
        # Render sidebar and get configuration
        sidebar_config = ui_service.render_sidebar()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # File upload section
            file_content = ui_service.render_file_upload()
            
            if file_content is not None:
                # Show processing button
                if st.button("🚀 Parse Resume", type="primary"):
                    
                    # Define processing stages for progress tracking
                    processing_stages = [
                        "Validating file",
                        "Extracting text from PDF", 
                        "Preparing document for analysis",
                        "Running AI analysis",
                        "Enhancing with retrieval data",
                        "Finalizing results"
                    ]
                    
                    # Create progress tracker
                    progress_tracker = ui_service.render_processing_progress(processing_stages)
                    
                    # Process the resume
                    try:
                        result = process_resume_file(
                            file_content=file_content,
                            filename="uploaded_resume.pdf",
                            options=sidebar_config,
                            progress_callback=lambda msg, prog: progress_tracker.update(msg, prog)
                        )
                        
                        # Complete progress
                        progress_tracker.complete()
                        
                        # Show document analysis if available
                        if result.document_analysis:
                            ui_service.render_document_analysis(result.document_analysis)
                        
                        # Show parsing results
                        ui_service.render_parsing_results(result, sidebar_config)
                        
                        # Show export options if successful
                        if result.success and result.data:
                            ui_service.render_export_options(result.data)
                        
                    except Exception as e:
                        progress_tracker.error(str(e))
                        ui_service.show_error("Processing failed", str(e))
                        logger.error(f"Resume processing failed: {str(e)}")
        
        with col2:
            # Statistics and information panel
            st.subheader("📊 Application Statistics")
            
            # Get application health
            try:
                health_status = orchestrator.get_application_health()
                
                # Show overall health
                health_icon = "🟢" if health_status["healthy"] else "🔴"
                st.metric("System Health", f"{health_icon} {'Healthy' if health_status['healthy'] else 'Issues'}")
                
                # Show session stats
                session_stats = health_status.get("session_stats", {})
                if session_stats:
                    st.metric("Documents Processed", session_stats.get("documents_processed", 0))
                    
                    success_rate = 0.0
                    if session_stats.get("documents_processed", 0) > 0:
                        success_rate = session_stats.get("successful_parses", 0) / session_stats["documents_processed"]
                    
                    st.metric("Success Rate", f"{success_rate:.1%}")
                
                # Show detailed health status in expander
                with st.expander("🔍 Detailed Health Status"):
                    services_health = health_status.get("services", {})
                    for service_name, service_health in services_health.items():
                        is_healthy = service_health.get("healthy", False)
                        status_icon = "✅" if is_healthy else "❌"
                        st.markdown(f"{status_icon} **{service_name.replace('_', ' ').title()}**: {'Healthy' if is_healthy else 'Issues'}")
                
            except Exception as e:
                st.error(f"Failed to get application status: {str(e)}")
        
        # Footer with additional information
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Status"):
                st.rerun()
        
        with col2:
            if st.button("🧹 Clear Caches"):
                try:
                    orchestrator.clear_caches()
                    ui_service.show_success("Caches cleared successfully")
                except Exception as e:
                    ui_service.show_error("Failed to clear caches", str(e))
        
        with col3:
            if st.button("📈 View Statistics"):
                try:
                    stats = orchestrator.get_processing_statistics()
                    with st.expander("📊 Detailed Statistics", expanded=True):
                        st.json(stats)
                except Exception as e:
                    ui_service.show_error("Failed to get statistics", str(e))
    
    except Exception as e:
        st.error(f"❌ Application initialization failed: {str(e)}")
        logger.error(f"Application failed to start: {str(e)}")
        
        # Show basic error recovery options
        st.markdown("### 🔧 Troubleshooting")
        st.markdown("""
        **If you're seeing this error, try:**
        1. Refresh the page
        2. Check that all required services are running
        3. Verify your configuration files
        4. Check the application logs for more details
        """)

if __name__ == "__main__":
    main()