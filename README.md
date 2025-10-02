# 🤖 Samantha — An AI Terminal Assistant for openEuler
> **OpenEuler Challenge Week Hackathon** | **Team: CodersBlue** 🏆

## **Project Description**

**Samantha** is a "Her"-inspired AI terminal companion who brings conversational touch to the command line. Instead of needing to understand cryptic commands, Samantha listens to what you want in plain English, understands your intent, and safely gets things done for you—whether that's searching files, organising data, or fixing mistakes. She learns from context, helps you recover from errors, and even offers helpful suggestions. Samantha is more than a tool—she's a helpful partner who makes working with your system feel natural, safe, and easier.

## 🎯 **Competition Highlights**

**✅ Tier 1**: Navigation, file operations, safety confirmations  
**✅ Tier 2**: Advanced search, multi-step operations, contextual understanding  
**✅ Tier 3**: Content-aware search, self-correction  

### **🚀 Standout Features**
- **Self-Correction**: Fuzzy matching suggests corrections for typos automatically
- **Content-Aware Search**: Find files by content, not just filename
- **Multi-Step Intelligence**: "Find PDFs then copy them to backup  
- **Safety-First Design**: All destructive operations require confirmation

---

## 🔧 **Quick Start**

### **Connect to the Virtual Machine**
1. Open a Terminal
2. Connect to the VM

```bash
ssh -J <username>@eidf-gateway.epcc.ed.ac.uk <username>@<ip_address>
```

### **Installation & Docker Setup**
```bash
# 1. Clone the repository
git clone https://github.com/compsoc-oe-week/track1_CodersBlue.git
cd track1_CodersBlue

# 2. Build and start the Docker container (in detached mode)
sudo docker compose build && sudo docker compose up -d

# 3. Enter the running container (named 'oe' by default)
sudo docker exec -it oe bash
```

### **Step-by-Step: Environment Setup & Running Samantha**
```bash
# 4. (Inside the container) Set up Python virtual environment (recommended)
cd /work
python3 -m venv .venv
source .venv/bin/activate
cd /work/track1_CodersBlue

# 5. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt || pip install openai python-dotenv colorama

# 6. Set environment variables for AI mode
export OPENAI_API_KEY=EMPTY
export CODER_BASE_URL=http://YOUR_SERVER_IP:8000/v1
export CODER_MODEL_NAME="Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8"
```

### **Test Samantha**
```bash
# 7. Run Samantha (try a test command)
python -m src.cli.samantha "list files in demo_data"
```

---

## 🎮 **Demo Commands**

### **Tier 1: Basic Operations**
```bash
# Navigation and listing
python -m src.cli.samantha "list files in demo_data"

# File deletion (with warning)
python -m src.cli.samantha “Delete the file demo_data/newfile.txt.”
```

### **Tier 2: Advanced Intelligence**
```bash
# Advanced search with filters
python -m src.cli.samantha "find pdf files in demo_data"
python -m src.cli.samantha "find files larger than 1mb in demo_data"

# Multi-step operations (DEMONSTRATES ADVANCED INTELLIGENCE)
python -m src.cli.samantha "find pdf files in demo_data then move them to backup"
```

### **Tier 3: AI-Powered Features**
```bash
# Content-aware search (finds files by content, not filename)
python -m src.cli.samantha"search for buget in demo_data"

# Suggestions
python -m src.cli.samantha "copy file_that_doesnt_exist.txt to backup"
# → Samantha suggests similar filenames automatically

# Self-correction (Notices that "buget" should be "budget")
python -m src.cli.samantha "find buget in demo_data"
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
│   └── suggestions.py       # Proactive organisational intelligence
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

## 🏆 **Why Samantha**

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
- **Khalid Elbagir**
- **Zayn Sharif**
- **Adam Azeb**
- **Abdulwahid Yaich**
- **Nabeel Ahmad**

**Project Highlights:**
- **Modular Architecture**: Clean separation enabling parallel development
- **Advanced Features**: Self-correction, content-aware search, proactive suggestions
- **Professional Quality**: Comprehensive testing, documentation, and safety features
- **Innovation**: Beyond requirements with "Her"-inspired intelligence

---

## 📋 **Project Deliverables** ✅

### **✅ Complete Implementation**
- ✅ **Full Repository**: All source code professionally organised and documented
- ✅ **Team Attribution**: Complete team member names with roles and contributions
- ✅ **Project Description**: Revolutionary AI terminal assistant with comprehensive feature set
- ✅ **Installation Guide**: Clear step-by-step instructions for setup and execution

### **✅ Technical Deliverables**
- ✅ **All Tiers Complete**: Tier 1 (100%), Tier 2 (100%), Tier 3 (100%)
- ✅ **Working Demo**: Tested commands ready for live demonstration
- ✅ **openEuler Integration**: Native compatibility with provided endpoints
- ✅ **Safety Features**: Confirmation prompts and path validation implemented
- ✅ **Professional Documentation**: Comprehensive README with architecture and demo guides
- ✅ **Quality Assurance**: Unit tests and robust error handling throughout

---

## 🎯 **Demos**

**Opening:**
```bash
python -m src.cli.samantha "list files in demo_data"
```

**Tier 1 Demo:**
```bash
# Basic operations with safety
python -m src.cli.samantha "copy presentation-slides.pdf from demo_data to backup"
```

**Tier 2 Demo:**
```bash
# Advanced multi-step intelligence
python -m src.cli.samantha "find pdf files in demo_data then move them to backup"
```

**Tier 3 Demo:**
```bash
# Content-aware search
python -m src.cli.samantha "search for budget in demo_data"
```
