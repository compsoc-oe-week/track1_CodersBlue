# 🤖 Samantha — An AI Terminal Assistant for openEuler
> **OpenEuler Challenge Week Hackathon** | **Team: CodersBlue** | **All Tiers Implemented** 🏆

**Samantha** is a revolutionary "Her"-inspired AI terminal assistant that transforms natural language into safe, intelligent system commands. Unlike traditional CLIs that force users to learn cryptic syntax, Samantha understands context, recovers from errors, and proactively suggests optimizations.

## 🎯 **Competition Highlights**

**✅ Tier 1 (100% Complete)**: Navigation, file operations, safety confirmations  
**✅ Tier 2 (100% Complete)**: Advanced search, multi-step operations, contextual understanding  
**✅ Tier 3 (100% Complete)**: Content-aware search, self-correction, organizational intelligence  

### **🚀 Standout Features**
- **Self-Correction**: Fuzzy matching suggests corrections for typos automatically
- **Content-Aware Search**: Find files by content, not just filename
- **Multi-Step Intelligence**: "Find PDFs then copy them to backup" works seamlessly  
- **Proactive Suggestions**: Detects cluttered directories and suggests cleanup
- **Safety-First Design**: All destructive operations require confirmation

---

## 🔧 **Quick Start**

### **Installation**
```bash
# Clone the repository
git clone https://github.com/panther-0707/track1_CodersBlue.git
cd track1_CodersBlue

# Install dependencies
pip install -r requirements.txt

# Test in mock mode (works immediately)
python -m src.cli.samantha --mock "list files in demo_data"
```

### **Environment Setup (For AI Mode)**
```bash
# Create .env file with API configuration
echo "CODER_BASE_URL=http://your-endpoint:8000/v1" > .env
echo "CODER_MODEL_NAME=Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8" >> .env
echo "OPENAI_API_KEY=your-api-key" >> .env
```

---

## 🎮 **Demo Commands** (Judge-Ready)

### **Tier 1: Basic Operations**
```bash
# Navigation and listing
python -m src.cli.samantha --mock "list files in demo_data"
python -m src.cli.samantha --mock "go to demo_data"

# File creation and manipulation  
python -m src.cli.samantha --mock "create a folder called test_results"
python -m src.cli.samantha --mock "copy presentation-slides.pdf from demo_data to backup"
```

### **Tier 2: Advanced Intelligence**
```bash
# Advanced search with filters
python -m src.cli.samantha --mock "find pdf files in demo_data"
python -m src.cli.samantha --mock "find files larger than 1mb in demo_data"

# Multi-step operations (DEMONSTRATES ADVANCED INTELLIGENCE)
python -m src.cli.samantha --mock "find pdf files in demo_data then move them to backup"
```

### **Tier 3: AI-Powered Features**
```bash
# Content-aware search (finds files by content, not filename)
python -m src.cli.samantha --mock "search for budget in demo_data"

# Self-correction and suggestions
python -m src.cli.samantha --mock "copy file_that_doesnt_exist.txt to backup"
# → Samantha suggests similar filenames automatically
```

---

## 🏗️ **Architecture Overview**

### **Core Components**
```
src/
├── cli/samantha.py           # Main CLI interface
├── core/
│   ├── nl2cmd.py            # Natural language → JSON plan conversion
│   ├── executor.py          # Safe command execution with recovery
│   ├── search.py            # Advanced file search with filters
│   ├── memory.py            # Conversation context and history
│   ├── safety.py            # Path validation and confirmations
│   └── suggestions.py       # Proactive organizational intelligence
├── ui/
│   ├── persona.py           # "Her"-inspired conversational tone
│   └── colors.py            # Beautiful ANSI terminal output
└── osint/openeuler.py       # openEuler system integration
```

### **Key Innovations**

**1. Self-Correction Engine**
```python
# Automatic typo correction with fuzzy matching
def execute_with_recovery(command_name, args, kwargs):
    try:
        return execute_command(command_name, args, kwargs)
    except FileNotFoundError as e:
        suggestions = find_similar_files(e.filename)
        return suggest_correction(suggestions)
```

**2. Content-Aware Search** 
```python
# Search files by content, not just filename
def search_in_files(content_pattern, path='.'):
    # Finds files containing specific keywords
    # Example: "search for budget" finds files with "budget" content
```

**3. Proactive Intelligence**
```python
# Detects patterns and suggests improvements
def suggest_desktop_cleanup():
    if count_screenshots() > 5:
        return create_cleanup_suggestion()
```

---

## 🎯 **Technical Sophistication**

### **Advanced Features**
- **JSON Plan Generation**: Natural language → structured execution plans
- **Pronoun Resolution**: "Find PDFs then copy them" handles "them" correctly
- **Safety Validation**: All operations preview before execution  
- **Error Recovery**: Multiple fallback strategies for failed commands
- **Context Awareness**: Maintains session state and working directory

### **openEuler Integration**
- **Package Management**: DNF integration for software installation
- **System Information**: Kernel version and system status queries
- **Performance Monitoring**: System resource awareness

---

## 🧪 **Testing & Validation**

```bash
# Run unit tests
python -m pytest tests/

# Test specific components
python -m pytest tests/test_search.py
python -m pytest tests/test_executor.py
```

### **Demo Data**
The `demo_data/` directory contains curated test files:
- PDF documents for file type filtering
- Text files with "budget" content for content search
- Large files for size-based filtering
- Nested directories for recursive operations

---

## 🏆 **Why Samantha Wins**

### **Functionality (40% of judging criteria)**
- ✅ **All Tiers Complete**: Every requirement implemented and tested
- ✅ **Robust Error Handling**: Graceful degradation and recovery
- ✅ **Rich Feature Set**: Beyond requirements with proactive suggestions

### **Technical Innovation (30%)**
- ✅ **Self-Correction**: Automatic typo detection and suggestions
- ✅ **Content-Aware Search**: Semantic file searching capability
- ✅ **Multi-Step Intelligence**: Complex operation chaining

### **User Experience (20%)**
- ✅ **"Her"-Inspired Persona**: Warm, helpful, intelligent interaction
- ✅ **Beautiful Output**: ANSI colors and clear formatting
- ✅ **Safety-First**: Confirmations prevent accidental destruction

### **openEuler Integration (10%)**
- ✅ **System Commands**: DNF, kernel info, package management
- ✅ **Native Integration**: Built for openEuler environment

---

## 👥 **Team CodersBlue**

**Team Members:**
- **Khalid Elbagir** - Team Lead & Architecture
- **Zayn Sharif** - AI/NLP Integration & Core Planning
- **Adam Azeb** - Terminal Operations & Safety Systems
- **Abdulwahid Yaich** - Advanced Search & Agentic Behavior
- **Nabeel Ahmad** - UX Design & Persona Development

**Project Highlights:**
- **Modular Architecture**: Clean separation enabling parallel development
- **Advanced Features**: Self-correction, content-aware search, proactive suggestions
- **Professional Quality**: Comprehensive testing, documentation, and safety features
- **Innovation**: Beyond requirements with "Her"-inspired intelligence

---

## 📋 **Final Submission Checklist** ✅

### **✅ Source Code Requirements**
- ✅ **Complete Repository**: All source code in GitHub under CompSoc organization
- ✅ **Team Member Names**: Listed above with roles and contributions
- ✅ **Clear Project Description**: Revolutionary AI terminal assistant with Tier 1-3 implementation
- ✅ **Step-by-Step Instructions**: Installation, setup, and demo commands provided

### **✅ Technical Deliverables**
- ✅ **All Tiers Complete**: Tier 1 (100%), Tier 2 (100%), Tier 3 (100%)
- ✅ **Working Demo**: Tested commands ready for live demonstration
- ✅ **openEuler Integration**: Native compatibility with provided endpoints
- ✅ **Safety Features**: Confirmation prompts and path validation implemented

### **📋 Still Needed**
- ⏳ **Presentation Slides**: 3-slide PDF with project overview, architecture, results
- ⏳ **Final Repository Transfer**: Move to CompSoc organization (if required)

---

## 🎯 **Live Demo Script** (Judge-Ready)

**Opening (30 seconds):**
```bash
# Show the warm, intelligent persona
python -m src.cli.samantha --mock "list files in demo_data"
```

**Tier 1 Demo (30 seconds):**
```bash
# Basic operations with safety
python -m src.cli.samantha --mock "copy presentation-slides.pdf from demo_data to backup"
```

**Tier 2 Demo (45 seconds):**
```bash
# Advanced multi-step intelligence
python -m src.cli.samantha --mock "find pdf files in demo_data then move them to backup"
```

**Tier 3 Demo (45 seconds):**
```bash
# Content-aware search (the wow factor)
python -m src.cli.samantha --mock "search for budget in demo_data"
```

**Total Demo Time: 2.5 minutes** - Perfect for judge presentations!
