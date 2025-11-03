# 🚀 Performance Tips for Resume Parser

## ⏰ Avoiding Timeouts

If you're experiencing timeout errors, try these solutions:

### 🎯 **Quick Fixes**

1. **Use a Faster Model**
   ```bash
   ollama pull phi3:mini        # Fastest (3.8GB)
   ollama pull gemma2:2b        # Lightweight (1.6GB)
   ```

2. **Reduce Document Size**
   - Split large documents into smaller sections
   - Remove unnecessary pages or content
   - Convert multi-page PDFs to single-page summaries

3. **Optimize Your System**
   - Close other applications to free memory
   - Ensure Ollama has enough system resources
   - Use SSD storage for better performance

### 📊 **Model Performance Comparison**

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `phi3:mini` | 3.8GB | ⚡⚡⚡ | ⭐⭐ | Fast processing, small docs |
| `gemma2:2b` | 1.6GB | ⚡⚡⚡ | ⭐⭐ | Very light, basic parsing |
| `llama3.2:3b` | 2GB | ⚡⚡ | ⭐⭐⭐ | Balanced speed/quality |
| `llama3.1:8b` | 4.7GB | ⚡ | ⭐⭐⭐⭐ | High quality, slower |

### 🔧 **Document Size Guidelines**

- **Small (< 2KB)**: Any model works fine
- **Medium (2-10KB)**: Use `phi3:mini` or `llama3.2:3b`
- **Large (> 10KB)**: Use `llama3.2:3b`, split if needed

### 🆘 **Troubleshooting Steps**

1. **Check Ollama Status**
   ```bash
   ollama list                 # See installed models
   ollama ps                   # See running models
   ```

2. **Test Model Speed**
   ```bash
   python recommend_model.py   # Run our speed test
   ```

3. **Monitor System Resources**
   - Check RAM usage (models need 4-8GB)
   - Ensure CPU isn't overloaded
   - Close unnecessary applications

### 💡 **Pro Tips**

- **For CVs/Resumes**: `phi3:mini` is usually fast enough
- **For Complex Documents**: Start with `llama3.2:3b`
- **If Still Timing Out**: Try processing smaller sections
- **Background Processing**: Let it run, Ollama will finish eventually

### 🎪 **Model Installation Commands**

```bash
# Fastest models (recommended)
ollama pull phi3:mini
ollama pull gemma2:2b

# Balanced model
ollama pull llama3.2:3b

# High-quality model (slower)
ollama pull llama3.1:8b
```

---

🚀 **The app automatically selects the best available model for your document size!**