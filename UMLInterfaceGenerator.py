import streamlit as st
import re
from plantuml import PlantUML


# PlantUML server for generating diagrams
plantuml_server = PlantUML(url="http://www.plantuml.com/plantuml/img/")

# Function to extract class, attributes, and methods info from Java code
def extract_class_info(java_code):
    classes = {}

    # Regex for class, attributes, and methods
    class_pattern = r'(class|interface)\s+(\w+)(?:\s+(implements|extends)\s+[\w\s,]+)?\s*{'
    attribute_pattern = r'(public|private|protected)?\s*(static\s+|final\s+|abstract\s+)*(\w+)\s+(\w+)(?:\s*=\s*[^,;]+)?;'
    method_pattern = r'(public|private|protected)?\s*(static\s+|final\s+|abstract\s+)*(\w+)\s+(\w+)\s*\((.*?)\)\s*(?:\{|;)'


    current_class = None
    class_type = None
    in_method = False  # Flag to track whether we're inside a method
    lines = java_code.splitlines()
    

    for line in lines:
        # Check for class name
        class_match = re.search(class_pattern, line)
        if class_match:
            class_type, class_name = class_match.groups()[0:2]
            current_class = class_name  # Get the class name
            classes[current_class] = {'Type': class_type, 'attributes': [], 'methods': []}

        if current_class:
            # Check for method
            method_match = re.search(method_pattern, line)
            if method_match:
                visibility, modifier, return_type, method_name, params = method_match.groups()
                if(modifier) == 'final ': method_name = method_name.upper()
                # Skip constructor methods
                if method_name == current_class:
                    continue

                classes[current_class]['methods'].append({
                    'visibility': visibility,
                    'modifier': modifier or '',
                    'return_type': return_type,
                    'name': method_name,
                    'parameters': params
                })

            # Check for attributes
            attr_match = re.search(attribute_pattern, line)
            if attr_match:
                visibility, modifier, attr_type, attr_name = attr_match.groups()
                if(modifier) == 'final ': attr_name = attr_match.upper()
                classes[current_class]['attributes'].append({
                    'visibility': visibility,
                    'modifier': modifier or '',
                    'type': attr_type,
                    'name': attr_name
                })

                
                

    return classes


# Function to generate PlantUML code including attributes, methods, and inheritance
def generate_plantuml(classes):
    plantuml_code = "skinparam classAttributeIconSize 0\n@startuml\n"
    
    for cls, details in classes.items():
        plantuml_code += f"{details['Type']} {cls} {{\n"
        
        # Add attributes
        for attr in details['attributes']:
            visibility_symbol = '-' if attr['visibility'] == 'private' else '#' if attr['visibility'] == 'protected' else '+'
            modifier_symbol = '{static} ' if 'static' in attr['modifier'] else ''
            plantuml_code += f"    {visibility_symbol} {modifier_symbol}{attr['name']} : {attr['type']}\n"
        
        # Add methods
        for method in details['methods']:
            visibility_symbol = '-' if method['visibility'] == 'private' else '#' if method['visibility'] == 'protected' else '+'
            modifier_symbol = '{static} ' if 'static' in method['modifier'] else '{abstract} ' if 'abstract' in method['modifier'] else ''
            
            # Format parameters as `name : type`
            param_list = []
            if method['parameters']:
                params = method['parameters'].split(',')
                for param in params:
                    param_type, param_name = param.strip().rsplit(' ', 1)
                    param_list.append(f"{param_name} : {param_type}")
            
            formatted_params = ", ".join(param_list)
            plantuml_code += f"    {visibility_symbol} {modifier_symbol}{method['name']}({formatted_params}) : {method['return_type']}\n"
        
        plantuml_code += "}\n"
    
    plantuml_code += "@enduml"
    return plantuml_code


# Function to generate UML diagram from PlantUML code
def generate_uml_diagram(uml_text):
    diagram_url = plantuml_server.get_url(uml_text)
    return diagram_url

def main():
    # Step 1: Upload the Java file
    uploaded_file = st.file_uploader("Choose a Java file", type="java")

    if uploaded_file is not None:
        # Read the uploaded file content
        java_code = uploaded_file.read().decode('utf-8')
        st.text_area("Uploaded Java File Content", java_code, height=300)

        # Step 2: Extract class info from Java code
        class_info = extract_class_info(java_code)
        st.write("Classes Found with Attributes and Methods:", class_info)
        #print(class_info)
        # Step 3: Generate PlantUML code
        plantuml_code = generate_plantuml(class_info)
        st.text_area("Generated PlantUML Code", plantuml_code, height=200)

        # Step 4: Generate and display UML diagram
        if st.button("Generate Class Diagram"):
            uml_diagram_url = generate_uml_diagram(plantuml_code)
            st.image(uml_diagram_url)

if __name__ == "__main__":
    main()
