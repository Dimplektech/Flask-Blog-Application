# Flask Blog Application

A feature-rich blogging platform implemented using Flask. This application is designed to provide a robust, user-friendly interface for creating, managing, and viewing blog posts. It features secure user authentication, rich text editing, and a responsive design.

---

## Features

### User Authentication
- Secure registration and login system with password hashing.
- User session management via Flask-Login.
- Admin privileges for managing posts.

### Blog Post Management
- Create, edit, and delete blog posts (admin only).
- View all posts on the homepage.

### Commenting System
- Authenticated users can add comments to posts.
- Users can delete their own comments.

### Profile Avatars
- Integrated Gravatar for user profile images.

### Rich Text Editing
- CKEditor integration for creating and editing posts.

### Responsive UI
- Fully responsive design using Bootstrap 5.

---

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip (Python package installer)

### Setup Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/flask-blog-app.git
    cd flask-blog-app
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

6. Access the application at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage

### Routes

- `/` : Homepage displaying all blog posts.
- `/register` : Register a new user.
- `/login` : Log in an existing user.
- `/logout` : Log out the current user.
- `/post/<int:post_id>` : View a specific blog post.
- `/new-post` : Create a new blog post (admin only).
- `/edit-post/<int:post_id>` : Edit an existing post (admin only).
- `/delete/<int:post_id>` : Delete a blog post (admin only).
- `/delete/comment/<int:comment_id>/<int:post_id>` : Delete a comment (comment owner only).
- `/about` : About page.
- `/contact` : Contact page.

### Admin User
- The first registered user is designated as the admin.

### Comment Management
- Authenticated users can comment on blog posts and delete their own comments.

---

## Database Models

### User
- **id**: Integer, primary key.
- **email**: String, unique identifier for the user.
- **password**: String, hashed password.
- **name**: String, user's display name.

### BlogPost
- **id**: Integer, primary key.
- **title**: String, unique title of the post.
- **subtitle**: String, short description.
- **date**: String, publication date.
- **body**: Text, the main content.
- **author**: String, author’s name.
- **img_url**: String, URL of the post’s featured image.
- **author_id**: Integer, foreign key referencing the User table.

### Comment
- **id**: Integer, primary key.
- **text**: Text, the comment content.
- **author_id**: Integer, foreign key referencing the User table.
- **post_id**: Integer, foreign key referencing the BlogPost table.

---

## Technologies Used

### Backend
- Flask: Web framework
- Flask-Login: User session management
- Flask-SQLAlchemy: ORM for database interactions
- CKEditor: Rich text editor

### Frontend
- Bootstrap 5: Responsive UI framework

### Database
- SQLite: Lightweight database for development

### Additional Tools
- Gravatar: Profile image integration
- Flask-Bootstrap: Simplifies UI styling

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Description of changes"
    ```
4. Push to your fork:
    ```bash
    git push origin feature-branch-name
    ```
5. Open a pull request on the main repository.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contact

For inquiries, please contact:
- GitHub: https://github.com/Dimplektech

