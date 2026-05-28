import customtkinter as ctk

from generator import generate_password

from vault import (
    view_credentials_file,
    add_credential_gui,
    security_audit
)
from auth import verify_master_password

# App appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LoginWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SecureVault Login")
        self.geometry("400x300")

        title = ctk.CTkLabel(
            self,
            text="SecureVault",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=(40, 20))

        subtitle = ctk.CTkLabel(
            self,
            text="Enter Master Password",
            font=("Arial", 16)
        )

        subtitle.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Master Password",
            show="*",
            width=250
        )

        self.password_entry.pack(pady=10)

        login_button = ctk.CTkButton(
            self,
            text="Unlock Vault",
            command=self.login
        )

        login_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(
            self,
            text=""
        )

        self.status_label.pack()

    def login(self):

        password = self.password_entry.get()

        if verify_master_password(password):

            self.destroy()

            app = SecureVaultApp()
            app.mainloop()

        else:

            self.status_label.configure(
                text="Incorrect master password."
            )


class SecureVaultApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window setup
        self.title("SecureVault")
        self.geometry("900x500")

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=200,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # Logo label
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="SecureVault",
            font=("Arial", 24, "bold")
        )

        self.logo_label.pack(
            pady=(30, 20)
        )

        # Add Credential button
        self.add_button = ctk.CTkButton(
            self.sidebar,
            text="Add Credential",
            command=self.show_add_credential
        )

        self.add_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # View Vault button
        self.view_button = ctk.CTkButton(
            self.sidebar,
            text="View Vault",
            command=self.show_vault
        )

        self.view_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # Generate Password button
        self.generate_button = ctk.CTkButton(
            self.sidebar,
            text="Generate Password",
            command=self.show_password_generator
        )

        self.generate_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # Security Audit button
        self.audit_button = ctk.CTkButton(
            self.sidebar,
            text="Security Audit",
            command=self.show_security_audit
        )

        self.audit_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # Main frame
        self.main_frame = ctk.CTkFrame(self)

        self.main_frame.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

        # Welcome label
        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text="Welcome to SecureVault",
            font=("Arial", 28, "bold")
        )

        self.welcome_label.pack(
            pady=(100, 10)
        )

        self.description_label = ctk.CTkLabel(
            self.main_frame,
            text=(
                "Your encrypted password manager\n"
                "built with Python and cybersecurity principles."
            ),
            font=("Arial", 16)
        )

        self.description_label.pack()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # =========================
    # PASSWORD GENERATOR
    # =========================

    def show_password_generator(self):

        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Password Generator",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=20)

        self.length_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter password length"
        )

        self.length_entry.pack(pady=10)

        generate_btn = ctk.CTkButton(
            self.main_frame,
            text="Generate",
            command=self.generate_password_action
        )

        generate_btn.pack(pady=10)

        self.password_output = ctk.CTkTextbox(
            self.main_frame,
            height=100,
            width=500
        )

        self.password_output.pack(pady=20)

    def generate_password_action(self):

        try:

            length = int(
                self.length_entry.get()
            )

            password = generate_password(length)

            self.password_output.delete(
                "1.0",
                "end"
            )

            self.password_output.insert(
                "end",
                password
            )

        except ValueError:

            self.password_output.delete(
                "1.0",
                "end"
            )

            self.password_output.insert(
                "end",
                "Please enter a valid number."
            )

    # =========================
    # VIEW VAULT
    # =========================

    def show_vault(self):

        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Stored Credentials",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=20)

        vault_text = ctk.CTkTextbox(
            self.main_frame,
            width=700,
            height=350
        )

        vault_text.pack(pady=10)

        credentials = view_credentials_file()

        vault_text.insert(
            "end",
            credentials
        )

    # =========================
    # SECURITY AUDIT
    # =========================

    def show_security_audit(self):

        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Security Audit",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=20)

        audit_box = ctk.CTkTextbox(
            self.main_frame,
            width=700,
            height=350
        )

        audit_box.pack(pady=10)

        results = security_audit()

        audit_box.insert(
            "end",
            results
        )
    # =========================
    # ADD CREDENTIAL
    # =========================

    def show_add_credential(self):

        self.clear_main_frame()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Add Credential",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=20)

        self.website_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Website",
            width=400
        )

        self.website_entry.pack(pady=10)

        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Username",
            width=400
        )

        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Password",
            width=400,
            show="*"
        )

        self.password_entry.pack(pady=10)

        save_button = ctk.CTkButton(
            self.main_frame,
            text="Save Credential",
            command=self.save_credential_action
        )

        save_button.pack(pady=20)

        self.save_status = ctk.CTkLabel(
            self.main_frame,
            text=""
        )

        self.save_status.pack()

    def save_credential_action(self):

        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = add_credential_gui(
            website,
            username,
            password
        )

        self.save_status.configure(
            text=result
        )


if __name__ == "__main__":

    login_window = LoginWindow()
    login_window.mainloop()