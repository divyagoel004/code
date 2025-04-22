import streamlit as st
import base64
import io
import chardet

def detect_encoding(binary_data):
    """Detect the encoding of the binary data."""
    detection = chardet.detect(binary_data)
    return detection['encoding'] if detection['encoding'] else 'utf-8'

def convert_buffer_to_text(buffer_data, encoding_type='auto'):
    """Convert buffer data to text using specified encoding."""
    try:
        if encoding_type == 'auto':
            encoding = detect_encoding(buffer_data)
        else:
            encoding = encoding_type
        
        # Try to decode the buffer using the detected or specified encoding
        text_content = buffer_data.decode(encoding)
        return True, text_content, encoding
    except Exception as e:
        return False, str(e), None

st.title("Buffer to Text Converter")
st.write("Paste a base64 encoded buffer to convert it to text")

# Create tab for base64 input
tab1 = st.tabs(["Base64 Input"])

with tab1[0]:  # Access the first tab
    # Using key parameter to track changes in the text_area
    base64_input = st.text_area("Paste Base64 encoded data here", key="base64_input_area", on_change=None)
    
    # Only process if there's input
    if base64_input:
        # Create encoding options
        encoding_options = ['auto', 'utf-8', 'ascii', 'latin-1', 'utf-16', 'utf-32']
        selected_encoding = st.selectbox("Select encoding (auto will attempt to detect)", encoding_options, key="base64_encoding")
        
        try:
            # Decode base64 to binary
            buffer_data = base64.b64decode(base64_input)
            
            success, result, detected_encoding = convert_buffer_to_text(buffer_data, selected_encoding)
            
            if success:
                st.success(f"Successfully converted using {detected_encoding} encoding")
                st.text_area("Text Output", result, height=400, disabled=False, key="output_area")
                st.download_button("Download as Text File", result, file_name="converted_text.txt")
            else:
                st.error(f"Error converting buffer: {result}")
        except Exception as e:
            st.error(f"Invalid Base64 input: {str(e)}")

st.divider()
st.write("This application converts binary data to text using various encodings.")
st.write("For optimal results with text files, try 'auto' detection first, then specific encodings if needed.")