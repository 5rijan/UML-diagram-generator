# UML Diagram Generator

This project is a web application that converts Java source code into UML diagrams. It uses Streamlit for the backend and UI, PlantUML to convert the text to the image, and a Java parser to parse the Java code to PlantUML syntax.

## Features

- **File Upload**: Users can upload `.java` files. The application will parse the Java code into PlantUML syntax and generate a UML diagram.
- **Customization**: Users can customize the theme of the UML diagram from a dropdown menu.
- **View and Download**: The UML diagram is displayed as a `.png` image which can be downloaded.
- **Manual Input**: Users can manually input PlantUML code into a text box to generate a diagram.

## Technologies Used

- **Streamlit**: Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. In this project, Streamlit is used for both the backend and the UI.
- **PlantUML**: PlantUML is an open-source tool that allows users to create UML diagrams from a plain text language. In this project, PlantUML is used to convert the PlantUML syntax into a UML diagram image.
- **Java Parser**: The Java parser is used to parse the Java source code into PlantUML syntax.

## How to Run

1. Clone this repository.
2. Install the required dependencies.
3. Run the `main.py` script.

## About the Developer

This application was developed by Srijan Chaudhary. For any queries or feedback, please reach out to me at [email](mailto:srijanchaudhary2003@gmail.com).

## Credits

This project wouldn't have been possible without the following open-source projects:

- **[PlantUML](http://plantuml.com/)**: An open-source tool that allows users to create UML diagrams from a plain text language. We use PlantUML to convert the PlantUML syntax into a UML diagram image.

- **[Java2PlantUML](https://github.com/mirajp1/java2plantuml.git)**: An initial parser that provided the base code for parsing Java source code into PlantUML syntax. We built upon this initial code to develop our application.

## License

This project is licensed under the terms of the MIT license.
