import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import google.generativeai as genai
import re
import os
import threading
import time
import json
from pathlib import Path
import random

class MultiAPISubtitleTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-API Subtitle Translator - Fast & Efficient")
        self.root.geometry("950x800")
        self.root.configure(bg='#2c3e50')
        
        # Configure fonts for Sinhala Unicode support
        self.setup_fonts()
        
        # Multiple API keys for rotation
        self.api_keys = [
            "key1",
            "key2", 
            "key3",
            "key4"
        ]
        
        self.current_api_index = 0
        self.models = {}
        self.setup_models()
        
        self.input_file = None
        self.output_file = None
        self.subtitles = []
        
        # Optimized settings
        self.batch_size = 15  # Larger batch size for faster processing
        self.max_retries = 3
        self.retry_delay = 1  # Shorter delay for retries
        
        self.translation_active = False
        self.completed_batches = 0
        
        self.title_colors = ["#FF0000", "#FF4500", "#FF6347", "#FF7F50", "#FF8C00"] # Red, OrangeRed, Tomato, Coral, DarkOrange
        self.current_title_color_index = 0
        
        self.setup_ui()
        self.animate_title_color() # Start the glitter effect
    
    def setup_fonts(self):
        """Setup fonts for Sinhala Unicode support"""
        try:
            # Try different Sinhala fonts
            sinhala_fonts = [
                "Noto Sans Sinhala",
                "Iskoola Pota", 
                "DL-Manel",
                "Malithi Web",
                "Potha",
                "Arial Unicode MS",
                "Segoe UI"
            ]
            
            # Test which font works
            import tkinter.font as tkFont
            for font_name in sinhala_fonts:
                try:
                    test_font = tkFont.Font(family=font_name, size=10)
                    self.sinhala_font = font_name
                    self.log_message(f"✅ Using Sinhala font: {font_name}")
                    break
                except:
                    continue
            else:
                self.sinhala_font = "Arial"
                self.log_message("⚠️ No Sinhala font found, using Arial")
                
        except Exception as e:
            self.sinhala_font = "Arial"
            self.log_message(f"⚠️ Font setup error: {str(e)}")
    
    def setup_models(self):
        """Initialize models for all API keys"""
        for i, api_key in enumerate(self.api_keys):
            try:
                genai.configure(api_key=api_key)
                self.models[i] = genai.GenerativeModel('gemini-2.0-flash-exp')
                self.log_message(f"✅ API Key {i+1} initialized successfully")
            except Exception as e:
                self.log_message(f"❌ Failed to initialize API Key {i+1}: {str(e)}")
    
    def get_next_model(self):
        """Get next available model with API key rotation"""
        self.current_api_index = (self.current_api_index + 1) % len(self.api_keys)
        
        # Configure the API key for this request
        try:
            genai.configure(api_key=self.api_keys[self.current_api_index])
            return self.models[self.current_api_index]
        except Exception as e:
            self.log_message(f"⚠️ Error switching to API key {self.current_api_index + 1}: {str(e)}")
            return self.models[0]  # Fallback to first model
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🚀 Multi-API Subtitle Translator", 
            font=("Arial", 22, "bold"),
            bg='#2c3e50',
            fg=self.title_colors[0] # Initial color red
        )
        title_label.pack(pady=20)
        self.title_label = title_label # Save reference to the label
        
        # API Status frame
        api_frame = tk.LabelFrame(
            self.root,
            text="API Keys Status",
            font=("Arial", 11, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        api_frame.pack(pady=10, padx=20, fill='x')
        
        self.api_status_label = tk.Label(
            api_frame,
            text=f"🔑 {len(self.api_keys)} API Keys Loaded | Current: Key 1",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#27ae60'
        )
        self.api_status_label.pack(pady=5)
        
        # Settings frame
        settings_frame = tk.LabelFrame(
            self.root,
            text="Processing Settings",
            font=("Arial", 11, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        settings_frame.pack(pady=10, padx=20, fill='x')
        
        settings_grid = tk.Frame(settings_frame, bg='#2c3e50')
        settings_grid.pack(fill='x', padx=10, pady=5)
        
        # Batch size
        tk.Label(
            settings_grid,
            text="Batch Size:",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).grid(row=0, column=0, sticky='w', padx=5)
        
        self.batch_size_var = tk.IntVar(value=15)
        tk.Spinbox(
            settings_grid,
            from_=10,
            to=50,
            width=8,
            textvariable=self.batch_size_var,
            font=("Arial", 10)
        ).grid(row=0, column=1, padx=5)
        
        # Auto key rotation
        self.auto_rotate_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            settings_grid,
            text="Auto API Key Rotation",
            variable=self.auto_rotate_var,
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            selectcolor='#34495e'
        ).grid(row=0, column=2, padx=20)
        
        # File selection frame
        file_frame = tk.Frame(self.root, bg='#2c3e50')
        file_frame.pack(pady=10, padx=20, fill='x')
        
        # Input file
        input_frame = tk.Frame(file_frame, bg='#2c3e50')
        input_frame.pack(fill='x', pady=5)
        
        tk.Label(
            input_frame, 
            text="English Subtitle File (.srt):", 
            font=("Arial", 11, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(anchor='w')
        
        input_file_frame = tk.Frame(input_frame, bg='#2c3e50')
        input_file_frame.pack(fill='x', pady=5)
        
        self.input_file_label = tk.Label(
            input_file_frame,
            text="No file selected",
            font=("Arial", 10),
            bg='#34495e',
            fg='#bdc3c7',
            relief='sunken',
            padx=10,
            pady=5
        )
        self.input_file_label.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Button(
            input_file_frame,
            text="📁 Browse",
            command=self.select_input_file,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            relief='flat',
            cursor='hand2'
        ).pack(side='right')
        
        # Output file
        output_frame = tk.Frame(file_frame, bg='#2c3e50')
        output_frame.pack(fill='x', pady=5)
        
        tk.Label(
            output_frame, 
            text="Output Sinhala Subtitle File:", 
            font=("Arial", 11, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(anchor='w')
        
        output_file_frame = tk.Frame(output_frame, bg='#2c3e50')
        output_file_frame.pack(fill='x', pady=5)
        
        self.output_file_label = tk.Label(
            output_file_frame,
            text="Auto-generated based on input file",
            font=("Arial", 10),
            bg='#34495e',
            fg='#bdc3c7',
            relief='sunken',
            padx=10,
            pady=5
        )
        self.output_file_label.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Button(
            output_file_frame,
            text="📁 Browse",
            command=self.select_output_file,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            relief='flat',
            cursor='hand2'
        ).pack(side='right')
        
        # Progress frame
        progress_frame = tk.Frame(self.root, bg='#2c3e50')
        progress_frame.pack(pady=20, padx=20, fill='x')
        
        # Main progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style='TProgressbar'
        )
        self.progress_bar.pack(fill='x', pady=5)
        
        # Status labels
        status_frame = tk.Frame(progress_frame, bg='#2c3e50')
        status_frame.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to translate",
            font=("Arial", 11, "bold"),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        self.status_label.pack(side='left')
        
        self.speed_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#3498db'
        )
        self.speed_label.pack(side='right')
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        self.translate_btn = tk.Button(
            button_frame,
            text="🚀 Start Fast Translation",
            command=self.start_translation,
            bg='#27ae60',
            fg='white',
            font=("Arial", 14, "bold"),
            padx=40,
            pady=12,
            relief='flat',
            cursor='hand2'
        )
        self.translate_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ Stop",
            command=self.stop_translation,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 14, "bold"),
            padx=40,
            pady=12,
            relief='flat',
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=10)
        
        # Log area
        log_frame = tk.LabelFrame(
            self.root,
            text="Translation Log",
            font=("Arial", 11, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        log_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            bg='#34495e',
            fg='#ecf0f1',
            font=(self.sinhala_font, 10),
            wrap='word'
        )
        self.log_text.pack(fill='both', expand=True, pady=5, padx=5)
        
        # Initialize log
        self.log_message("🎬 Multi-API Subtitle Translator Ready!")
        self.log_message(f"📊 {len(self.api_keys)} API keys loaded for maximum speed")
        self.log_message("සිංහල යුනිකෝඩ් සහාය සක්‍රිය කර ඇත")

    def animate_title_color(self):
        """Animates the title label's color for a glitter effect."""
        if hasattr(self, 'title_label'): # Ensure title_label exists
            self.current_title_color_index = (self.current_title_color_index + 1) % len(self.title_colors)
            new_color = self.title_colors[self.current_title_color_index]
            self.title_label.config(fg=new_color)
            self.root.after(500, self.animate_title_color) # Change color every 500ms
    
    def log_message(self, message):
        """Add message to log area"""
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)
            self.root.update_idletasks()
    
    def select_input_file(self):
        """Select input SRT file"""
        file_path = filedialog.askopenfilename(
            title="Select English Subtitle File",
            filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            self.input_file_label.config(text=os.path.basename(file_path))
            
            # Auto-generate output file name
            if self.output_file is None:
                base_name = Path(file_path).stem
                output_path = Path(file_path).parent / f"{base_name}_sinhala.srt"
                self.output_file = str(output_path)
                self.output_file_label.config(text=os.path.basename(self.output_file))
    
    def select_output_file(self):
        """Select output SRT file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Sinhala Subtitle File As",
            defaultextension=".srt",
            filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
        )
        if file_path:
            self.output_file = file_path
            self.output_file_label.config(text=os.path.basename(file_path))
    
    def parse_srt_file(self, file_path):
        """Parse SRT subtitle file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        blocks = re.split(r'\n\s*\n', content.strip())
        subtitles = []
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    index = int(lines[0])
                    timestamp = lines[1]
                    text = '\n'.join(lines[2:])
                    subtitles.append({
                        'index': index,
                        'timestamp': timestamp,
                        'text': text
                    })
                except ValueError:
                    continue
        
        return subtitles
    
    def create_batches(self, subtitles, batch_size):
        """Create batches of subtitles for processing"""
        batches = []
        for i in range(0, len(subtitles), batch_size):
            batches.append(subtitles[i:i + batch_size])
        return batches
    
    def translate_batch_with_retry(self, batch, batch_num, total_batches):
        """Translate a batch of subtitles with retry mechanism"""
        for attempt in range(self.max_retries):
            try:
                # Get next model (rotates API keys)
                if self.auto_rotate_var.get():
                    model = self.get_next_model()
                    self.api_status_label.config(text=f"🔑 Using API Key {self.current_api_index + 1}")
                else:
                    model = self.models[0]
                
                # Create batch prompt
                batch_text = ""
                for i, subtitle in enumerate(batch):
                    batch_text += f"[{i+1}] {subtitle['text']}\n\n"
                
                prompt = f"""Translate these English subtitles to Sinhala. Keep each translation natural and conversational, suitable for movie subtitles.
                Return them in the exact same format with [1], [2], etc. markers.
                
                {batch_text}
                
                Provide only the Sinhala translations with the same numbering, no explanations."""
                
                self.log_message(f"🔄 Processing batch {batch_num}/{total_batches} with API key {self.current_api_index + 1}")
                
                response = model.generate_content(prompt)
                translated_texts = self.parse_batch_response(response.text, len(batch))
                
                # Create translated batch
                translated_batch = []
                for i, subtitle in enumerate(batch):
                    translated_batch.append({
                        'index': subtitle['index'],
                        'timestamp': subtitle['timestamp'],
                        'text': translated_texts[i] if i < len(translated_texts) else subtitle['text']
                    })
                
                self.log_message(f"✅ Batch {batch_num} completed successfully")
                return translated_batch
                
            except Exception as e:
                error_msg = str(e).lower()
                if "rate limit" in error_msg or "quota" in error_msg:
                    self.log_message(f"⚠️ Rate limit hit on attempt {attempt + 1}, trying next API key...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.log_message(f"⚠️ Error in batch {batch_num}, attempt {attempt + 1}: {str(e)}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                    continue
        
        # If all retries failed, return original batch
        self.log_message(f"❌ Failed to translate batch {batch_num} after {self.max_retries} attempts")
        return batch
    
    def parse_batch_response(self, response_text, expected_count):
        """Parse batch translation response"""
        lines = response_text.strip().split('\n')
        translations = []
        current_translation = ""
        
        for line in lines:
            line = line.strip()
            if re.match(r'^\[\d+\]', line):
                if current_translation:
                    translations.append(current_translation.strip())
                current_translation = re.sub(r'^\[\d+\]\s*', '', line)
            else:
                if current_translation:
                    current_translation += "\n" + line
        
        if current_translation:
            translations.append(current_translation.strip())
        
        # Ensure we have the expected number of translations
        while len(translations) < expected_count:
            translations.append("Translation failed")
        
        return translations[:expected_count]
    
    def save_srt_file(self, subtitles, file_path):
        """Save translated subtitles to SRT file with proper UTF-8 encoding"""
        try:
            with open(file_path, 'w', encoding='utf-8-sig') as file:  # UTF-8 with BOM
                for subtitle in subtitles:
                    file.write(f"{subtitle['index']}\n")
                    file.write(f"{subtitle['timestamp']}\n")
                    file.write(f"{subtitle['text']}\n\n")
            self.log_message(f"💾 File saved with UTF-8 encoding: {os.path.basename(file_path)}")
        except Exception as e:
            self.log_message(f"❌ Error saving file: {str(e)}")
            raise
    
    def start_translation(self):
        """Start the translation process"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        if not self.output_file:
            messagebox.showerror("Error", "Please specify an output file")
            return
        
        self.translation_active = True
        self.translate_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.completed_batches = 0
        
        # Update batch size from UI
        self.batch_size = self.batch_size_var.get()
        
        # Start translation in separate thread
        thread = threading.Thread(target=self.translate_subtitles)
        thread.daemon = True
        thread.start()
    
    def stop_translation(self):
        """Stop the translation process"""
        self.translation_active = False
        self.translate_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Translation stopped")
        self.speed_label.config(text="")
        self.log_message("🛑 Translation stopped by user")
    
    def translate_subtitles(self):
        """Main translation function with batch processing"""
        try:
            start_time = time.time()
            
            self.log_message("🔍 Parsing subtitle file...")
            self.status_label.config(text="Parsing subtitle file...")
            
            # Parse input file
            subtitles = self.parse_srt_file(self.input_file)
            total_subtitles = len(subtitles)
            
            if total_subtitles == 0:
                self.log_message("❌ No subtitles found in file")
                self.stop_translation()
                return
            
            # Create batches
            batches = self.create_batches(subtitles, self.batch_size)
            total_batches = len(batches)
            
            self.log_message(f"📝 Found {total_subtitles} subtitle entries")
            self.log_message(f"📦 Created {total_batches} batches (batch size: {self.batch_size})")
            self.log_message(f"🔑 Using {len(self.api_keys)} API keys for rotation")
            
            # Process batches
            translated_subtitles = []
            
            for batch_num, batch in enumerate(batches, 1):
                if not self.translation_active:
                    break
                
                self.status_label.config(text=f"Processing batch {batch_num}/{total_batches}")
                
                # Translate batch
                translated_batch = self.translate_batch_with_retry(batch, batch_num, total_batches)
                translated_subtitles.extend(translated_batch)
                
                self.completed_batches += 1
                
                # Update progress
                progress = (self.completed_batches / total_batches) * 100
                self.progress_var.set(progress)
                
                # Calculate and display speed
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    subtitles_per_sec = (self.completed_batches * self.batch_size) / elapsed_time
                    self.speed_label.config(text=f"⚡ {subtitles_per_sec:.1f} subtitles/sec")
                
                # Small delay to prevent overwhelming the APIs
                if batch_num < total_batches:
                    time.sleep(0.2)
            
            if self.translation_active:
                # Save translated file
                self.log_message("💾 Saving translated subtitles...")
                self.status_label.config(text="Saving file...")
                
                self.save_srt_file(translated_subtitles, self.output_file)
                
                total_time = time.time() - start_time
                avg_speed = total_subtitles / total_time if total_time > 0 else 0
                
                self.log_message(f"🎉 Translation completed successfully!")
                self.log_message(f"📊 Processed {total_subtitles} subtitles in {total_time:.1f} seconds")
                self.log_message(f"⚡ Average speed: {avg_speed:.1f} subtitles/second")
                self.log_message(f"💾 Saved to: {self.output_file}")
                self.log_message("සිංහල උපසිරැසි සාර්ථකව නිර්මාණය කරන ලදී!")
                
                self.status_label.config(text="Translation completed successfully!")
                self.speed_label.config(text=f"⚡ Final: {avg_speed:.1f} subtitles/sec")
                
                messagebox.showinfo(
                    "Success!", 
                    f"Translation completed in {total_time:.1f} seconds!\n"
                    f"Speed: {avg_speed:.1f} subtitles/second\n"
                    f"Saved to: {os.path.basename(self.output_file)}"
                )
            
        except Exception as e:
            self.log_message(f"❌ Error during translation: {str(e)}")
            messagebox.showerror("Error", f"Translation failed: {str(e)}")
        
        finally:
            self.translate_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.translation_active = False

def main():
    root = tk.Tk()
    app = MultiAPISubtitleTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
