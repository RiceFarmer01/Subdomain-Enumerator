import dns.resolver
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar, Combobox

class SubdomainEnumerator:
    def __init__(self, root):
        self.root = root
        self.root.title('Subdomain Enumerator')
        self.root.geometry('400x480')
        self.root.configure(background='#2B2B2B')

        self.domain_label = tk.Label(root, text="Enter Domain", fg='white', bg='#2B2B2B', font=("Arial", 12))
        self.domain_entry = tk.Entry(root, fg='white', bg='#3C3F41', insertbackground='white')
        self.wordlist_label = tk.Label(root, text="Select Wordlist", fg='white', bg='#2B2B2B', font=("Arial", 12))
        self.wordlist_combobox = Combobox(root, values=["subdomains-100.txt", "subdomains-500.txt", "subdomains-1000.txt", "subdomains-10000.txt", "subdomains-uk-500.txt", "subdomains-uk-1000.txt"], state="readonly")
        self.custom_wordlist_button = tk.Button(root, text="Add Custom Wordlist", command=self.add_custom_wordlist, fg='white', bg='#3C3F41', activebackground='#4E4E4E', font=("Arial", 12))
        self.submit_button = tk.Button(root, text="Enumerate Subdomains", command=self.enumerate_subdomains, fg='white', bg='#3C3F41', activebackground='#4E4E4E', font=("Arial", 12))
        self.progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.subdomain_count_label = tk.Label(root, text="", fg='white', bg='#2B2B2B', font=("Arial", 12))
        self.accuracy_label = tk.Label(root, text="", fg='white', bg='#2B2B2B', font=("Arial", 12))
        self.made_by_frame = tk.Frame(root, bg='#2B2B2B')
        self.made_by_label = tk.Label(self.made_by_frame, text="Made by ", fg='white', bg='#2B2B2B', font=("Arial", 12))
        self.github_link = tk.Label(self.made_by_frame, text="Jaiden", fg='white', bg='#2B2B2B', font=("Arial", 12), cursor="hand2")
        self.github_link.bind("<Button-1>", lambda e: self.open_github_link())

        self.domain_label.pack(fill='x', padx=10, pady=5)
        self.domain_entry.pack(fill='x', padx=10, pady=5)
        self.wordlist_label.pack(fill='x', padx=10, pady=5)
        self.wordlist_combobox.pack(fill='x', padx=10, pady=5)
        self.custom_wordlist_button.pack(fill='x', padx=10, pady=5)
        self.submit_button.pack(fill='x', padx=10, pady=5)
        self.progress_bar.pack(pady=10)
        self.subdomain_count_label.pack(fill='x', padx=10, pady=5)
        self.accuracy_label.pack(fill='x', padx=10, pady=5)
        self.made_by_frame.pack(side='bottom', pady=5)
        self.made_by_label.pack(side='left')
        self.github_link.pack(side='left')

    def enumerate_subdomains(self):
        domain = self.domain_entry.get()
        if not domain:
            messagebox.showerror("Error", "Please enter a valid domain.")
            return

        wordlist = self.wordlist_combobox.get()
        if not wordlist:
            messagebox.showerror("Error", "Please select a wordlist.")
            return

        try:
            subdomains = self.brute_force_subdomains(domain, wordlist)
            subdomain_count = len(subdomains)

            with filedialog.asksaveasfile(mode='w', defaultextension=".txt") as output_file:
                output_file.write('\n'.join(subdomains))

            messagebox.showinfo("Success", "Subdomains written to file successfully.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return
        
        self.subdomain_count_label.config(text=f"Subdomains Found: {subdomain_count}")
        accuracy_percentage = 0 if not subdomain_count else (subdomain_count / self.total_domains) * 100
        self.accuracy_label.config(text=f"Accuracy: {accuracy_percentage:.2f}%")

    def brute_force_subdomains(self, domain, wordlist):
        with open(wordlist, 'r') as wordlist_file:
            subdomains = [line.strip() for line in wordlist_file]

        discovered_subdomains = []
        
        self.total_domains = len(subdomains)
        self.progress_bar['maximum'] = self.total_domains
        self.progress_bar['value'] = 0
        subdomain_count = 0
        
        for index, subdomain in enumerate(subdomains):
            try:
                result = dns.resolver.resolve(f"{subdomain}.{domain}", "A")
                for ipval in result:
                    discovered_subdomains.append(f"{subdomain}.{domain} {ipval.to_text()}")
                    subdomain_count += 1
            except:
                pass
            
            progress_percent = int((index + 1) / self.total_domains * 100)
            
            self.progress_bar['value'] = index + 1
            self.root.update_idletasks()
            
            accuracy_percentage = 0 if not subdomain_count else (subdomain_count / (index + 1)) * 100
            self.subdomain_count_label.config(text=f"Subdomains Found: {subdomain_count}")
            self.accuracy_label.config(text=f"Accuracy: {accuracy_percentage:.2f}%")
        
        return discovered_subdomains

    def add_custom_wordlist(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.wordlist_combobox['values'] = list(self.wordlist_combobox['values']) + [file_path]
            self.wordlist_combobox.set(file_path)

    def open_github_link(self):
        import webbrowser
        webbrowser.open("https://github.com/RiceFarmer01")

root = tk.Tk()
app = SubdomainEnumerator(root)
root.mainloop()