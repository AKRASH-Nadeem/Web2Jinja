# **Web2Jinja**
Web2Jinja is a powerful Python3 tool that simplifies the process of converting websites into Flask Jinja format. It is designed to streamline backend coding for Python developers, automating the conversion process and enabling them to focus on building robust Flask applications.

## **Features**
* **Effortless Conversion**: Web2Jinja effortlessly converts websites into Flask Jinja format, saving developers valuable time and effort.
* **HTML to Jinja Mapping**: The tool automatically maps HTML elements to their equivalent Jinja syntax, ensuring an accurate and reliable conversion.
* **Template Inheritance**: Web2Jinja handles template inheritance, making it easy to structure and organize your Flask Jinja templates.
* **Navigation Bar in Separate File**: The tool provides the ability to extract the navigation bar into a separate file, promoting code reusability and maintainability.
* **Route Creation**: Web2Jinja generates a Python file that includes all the routes, connecting them to the templates.
* **Static File Linking**: The tool automatically links the static files (CSS, JavaScript, images, etc.) to the Flask application.

## **Getting Started**
1. Ensure you have Python 3.x installed on your system.
2. Clone the repository:
    ```bash
    git clone https://github.com/AKRASH-Nadeem/Web2Jinja.git
    ```
3. Install the required dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
4. Run the Web2Jinja script:
    ```bash
    python3 web2jinja.py
    ```
The script will prompt you for the following information:
* Path to the website you want to convert
* Folder name for the Flask Jinja templates (e.g., enter "my_website_flask" for "my_website" folder)

    The converted Flask Jinja templates will be generated within a folder named "<folder_name>_flask" in the same location as the original website. Additionally, a Python file will be created, containing all the routes connected to the templates and the automatic linking of static files.

5. **Start building your Flask application**:
    With the converted Flask Jinja templates, including the separate navigation bar file if applicable, you are now ready to start building your Flask application. Utilize the power of Flask and Jinja to develop dynamic and interactive web applications with ease.
## **Contributing**
Contributions to Web2Jinja are welcome! If you find any bugs or have suggestions for new features, please open an issue or submit a pull request on the GitHub repository.

Before making a contribution, please review the [contribution guidelines](./CONTRIBUTING.md) for detailed information on the process.
## **License**
This project is licensed under the [MIT License](./LICENSE).
## **Acknowledgements**
Web2Jinja was inspired by the need to simplify the process of converting websites into Flask Jinja format. We would like to express our gratitude to the open-source community for their invaluable contributions and support.
## **Contact**
For any questions or inquiries, please [Contact](mailto:princecharmieonwork@gmail.com).

Happy Flask coding with Web2Jinja!