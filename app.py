import os
import streamlit as st

st.set_page_config(
    page_title="Třídič fotek",
    page_icon="📷",
    layout="wide"
)

with st.sidebar:
    st.title("Třídič fotek")
    input_folder = st.text_input("Vyberte složku, která se bude procházet", value=r"C:\Users\jaroslav\Pictures")
    output_folder = st.text_input("Vyberte složku, kam se budou ukládat výstupy", value=r"C:\Users\jaroslav\Downloads")

if input_folder and output_folder:
    if not os.path.exists(input_folder):
        st.error("Zadaná vstupní složka neexistuje. Opravte prosím cestu.")
    elif not os.path.exists(output_folder):
        st.error("Zadaná výstupní složka neexistuje. Opravte prosím cestu.")
    else:
        with st.sidebar:
            st.write(f"Prohledávám složku: {input_folder}")
        # Create the output folder structure
        output_base = os.path.join(output_folder, 'FaceCollector_output')
        
        with st.sidebar:
            folder_names = st.text_area(
                "Zadejte názvy složek oddělené čárkou (např. Yes, Maybe, No):",
                value="Yes, Maybe, No"
            ).split(',')

            folder_names = [name.strip() for name in folder_names if name.strip()]  # Clean up names and remove empty ones

            folders = {}
            for folder_name in folder_names:
                folder_path = os.path.join(output_base, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                folders[folder_name] = folder_path

        # Get a list of all image files in the input folder and subfolders
        image_files = []
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.raw', '.svg')):
                    image_files.append(os.path.join(root, file))

        # Use session state to keep track of the current image index
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0

        if st.session_state.current_index < len(image_files):
            current_file = image_files[st.session_state.current_index]
            st.subheader(current_file)  # Display the file path in the Streamlit app
          
            cols = st.columns(len(folders))
            for i, (folder_name, folder_path) in enumerate(folders.items()):
                if cols[i].button(f"{folder_name}", type="primary", use_container_width=True):
                    destination = os.path.join(folder_path, os.path.basename(current_file))
                    if not os.path.exists(destination):
                        with open(current_file, 'rb') as src, open(destination, 'wb') as dst:
                            dst.write(src.read())
                        st.toast(f"Soubor {os.path.basename(current_file)} byl zkopírován do složky {folder_name}.")
                        st.session_state.current_index += 1
                        st.rerun()
            try:
                st.image(current_file, caption=os.path.basename(current_file), use_container_width=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
        else:
            st.write("Všechny obrázky byly zpracovány.")     