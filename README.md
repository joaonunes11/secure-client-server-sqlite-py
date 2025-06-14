# Secure Client-Server Application with SQLite and SSL (Python)

This project implements a secure client-server system using Python, SQLite, and SSL/TLS encryption. The application allows the management of users, bands, and albums via terminal-based commands, with secure communication between client and server.

## 📌 Project Objective

To develop a secure client-server application with encrypted communication and persistent storage, simulating a simple music database management system.

## 🔒 Security

- SSL/TLS encryption with self-signed certificates
- Custom certificate authority (`certs/CA.crt`)
- Encrypted communication between client and server using Python's `ssl` module

## 🧱 Architecture

- **Client (`client/client.py`)**: Connects to the server securely and sends commands.
- **Server (`server/server.py`)**: Processes requests using SQLite and responds to the client.
- **Database (`server/ad14.db`)**: Stores all records (users, bands, albums).
- **SQL Schema (`server/ad14.sql`)**: Database structure initialization.
- **SQLite Helper (`server/sqlite.py`)**: Performs operations on the database.
- **Certificates (`certs/`)**: Contains all required `.crt` and `.key` files.

## 🔧 Technologies Used

- Python 3.x
- SQLite
- SSL/TLS
- `socket` and `ssl` modules

## 🚀 How to Run

1. Run the secure server:
```bash
cd server
python3 server.py
```

2. In another terminal, run the secure client:
```bash
cd client
python3 client.py
```

⚠️ Make sure the `certs/` folder is accessible in both client and server directories.

## 🗂️ Command Examples

- `ADD USER <username> <password> <name>`
- `SHOW ALBUM <id>`
- `REMOVE BANDAS`, `REMOVE USER <id>` ...

*(See `Enunciado.pdf` for full list of commands.)*

## 📄 Documentation

- `README.md` – current file
- `Enunciado.pdf` – official assignment statement

## 👩‍💻 Author

- João Nunes
- André Ramos

## 📃 License

This project is for academic and educational use only.
