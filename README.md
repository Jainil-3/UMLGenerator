# UMLGenerator

## Overview

This project provides a web-based application using **Streamlit** that generates UML class diagrams from Java code. The tool parses Java classes and interfaces, extracts relevant information such as attributes and methods, and then generates PlantUML code, which is converted into a UML class diagram. The project is built to handle both **Java classes** and **interfaces**, ensuring proper visualization of attributes, methods, and relationships.

## Features

- **Supports Java Classes and Interfaces:** The tool extracts both class and interface information.
- **Method and Attribute Parsing:** Parses and displays class attributes and methods, including visibility, return types, and parameters.
- **PlantUML Integration:** Automatically generates UML diagrams from the extracted class information using the PlantUML web server.
- **Streamlit UI:** Provides a simple web interface to upload Java files and generate UML diagrams on the fly.

## Project Structure

- `extract_class_info`: A function to extract information about Java classes and interfaces, including attributes and methods.
- `generate_plantuml`: Converts the parsed Java class data into PlantUML code.
- `generate_uml_diagram`: Uses PlantUML to generate a UML class diagram.
- **Streamlit UI**: Provides a web interface for uploading Java files and generating class diagrams.

## Requirements

- Python 3.x
- Required Python Libraries:
  - `streamlit`
  - `re`
  - `plantuml`
  - `requests`

## Setup Instructions

1. **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    - **Required Dependencies:**
      - `streamlit` (for building the UI)
      - `re` (for regular expression parsing)
      - `plantuml` (for generating UML diagrams)
      - `requests` (required for PlantUML API)

3. **Run the Application:**
    ```bash
    streamlit run UMLClassGenerator.py
    ```

4. **Upload a Java File:**
    - Once the application is running, upload your Java file using the provided UI.
    - The application will extract class, attribute, and method information and display the corresponding UML diagram.

## Code Walkthrough

### 1. `extract_class_info`
This function is responsible for parsing Java code and extracting the following information:
- **Classes and Interfaces**: Both class and interface definitions are identified using regex.
- **Attributes**: Class variables are parsed along with their visibility (`public`, `private`, `protected`), modifiers (`static`, `final`), and data types.
- **Methods**: Methods are parsed, and details such as visibility, modifiers, return type, and parameters are extracted.

#### Regular Expressions:
- **Class/Interface**: 
  ```python
  class_pattern = r'(class|interface)\s+(\w+)(?:\s+(implements|extends)\s+[\w\s,]+)?\s*{'
  ```
  This regex identifies whether the Java type is a class or an interface.
  
- **Attributes**: 
  ```python
  attribute_pattern = r'(public|private|protected)?\s*(static\s+|final\s+|abstract\s+)*(\w+)\s+(\w+)(?:\s*=\s*[^,;]+)?;'
  ```
  This pattern identifies variables, their visibility, type, and name.

- **Methods**: 
  ```python
  method_pattern = r'(public|private|protected)?\s*(static\s+|final\s+|abstract\s+)*(\w+)\s+(\w+)\s*\((.*?)\)\s*(?:\{|;)'
  ```
  This pattern identifies methods, their visibility, return type, method name, and parameters. It handles both concrete methods (denoted by `{`) and interface methods (denoted by `;`).

### 2. `generate_plantuml`
This function converts the extracted class information into valid **PlantUML** code, which is then used to generate the UML diagram. The attributes and methods are formatted according to the UML standard.

### 3. `generate_uml_diagram`
This function uses the **PlantUML** web service to convert the generated PlantUML code into an image of the UML diagram.

### 4. **Streamlit UI**
The `main()` function sets up a simple **Streamlit** user interface, which allows users to upload a Java file. It then displays the extracted information, generates PlantUML code, and renders the UML diagram.

### Handling Interfaces
A separate class handles interfaces in a manner similar to regular classes, ensuring methods defined in interfaces are properly parsed and displayed in the UML diagram. The distinction between `class` and `interface` is made using the `class_pattern` regex.

```python
class_pattern = r'(class|interface)\s+(\w+)(?:\s+(implements|extends)\s+[\w\s,]+)?\s*{'
```

The rest of the logic remains similar, with the code checking whether the current Java type is a class or an interface.

## Example

For a Java class:

```java
public class MyClass {
    private String name;
    public int age;

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

The generated UML diagram will display:
- Attributes:
  - `- name : String`
  - `+ age : int`
- Methods:
  - `+ setName(name : String) : void`
  - `+ getName() : String`

## Known Issues and Future Improvements
- Currently, the tool does not support nested classes.
- An additional improvement would be the ability to handle more complex inheritance and relationships between classes.

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue for any improvements or suggestions.
