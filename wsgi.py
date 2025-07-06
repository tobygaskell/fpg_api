"""WSGI entry point for the fpg_api application."""

from fpg_api.app import app

if __name__ == "__main__":
    app.run()
