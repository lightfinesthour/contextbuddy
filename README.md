**Context Buddy: A Code Analysis and Question Answering Tool** or Simple Python Script that uses a LLM to answer question about your code.

**Overview**
-----------

The Context Tester is a Python-based tool that analyzes code files, combines their contents into a single string, and then uses the OpenAI API to answer questions about the code. The tool supports multiple programming languages, including Python, C# MAUI, JavaScript, Java, and others.

**Features**
-------------

### Language Support

The Context Tester currently supports the following programming languages:

*   Python
*   C# MAUI
*   JavaScript
*   Java
*   Other (only .txt files)

### Code Analysis

The tool recursively searches through a specified directory for files with extensions specific to each supported language. It then reads and combines the contents of these files into a single string.

### Question Answering

Using the OpenAI API, the Context Tester answers questions about the combined code content. You can ask questions like "What is this code doing?" or "How does this function work?"

**Usage**
---------

1.  Clone the repository to your local machine.
2.  Run the script by executing `python context_tester.py`.
3.  Specify the language of the code files when prompted.
4.  Enter a question about the code, and the Context Tester will provide an answer (depending on the LLM active in LM-Studio or other).

**Configuration**
--------------

### Setup LM-Studio

Go to the server tab and start the server.

### Environment Variables

You can configure the Context Tester by setting environment variables:

*   `OPENAI_SERVER_URL`: The URL of your local OpenAI server (e.g., `http://localhost:1234/v1`).

**License**
---------

The Context Tester is licensed under the [MIT License](LICENSE).

**Contributing**
-------------

Contributions to the Context Tester are welcome! If you'd like to add new language support, improve the code analysis or question answering capabilities, or fix bugs, please submit a pull request.
