import tkinter as tk
from tkinter import ttk, messagebox

class GloomhavenEnemyManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gloomhaven Enemy Manager")
        self.root.geometry("1100x850")
        
        # Configure colors
        self.bg_color = "#664C4C"  # Deep maroon
        self.normal_color = "#d3d3d3"  # Light gray for normal enemies
        self.elite_color = "#ffd700"  # Gold for elite enemies
        self.boss_color = "#6161C7"  # Dark blue for bosses
        self.card_bg = "#f8f8f8"
        self.header_color = "#B3132E"
        self.text_color = "black"  # Text color changed to black
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"), background=self.header_color, foreground="white")
        self.style.configure("TButton", background="#444", foreground=self.text_color)
        self.style.configure("TLabelFrame", background=self.bg_color, foreground="white")
        self.style.configure("TLabelFrame.Label", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TCheckbutton", background=self.bg_color, foreground=self.text_color)
        
        # Set background color
        root.configure(background=self.bg_color)
        
        # Create main panels
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.configure(style="TFrame")
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Create control frame for level selection and add enemy button
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.control_frame.configure(style="TFrame")
        
        # Level selection dropdown
        ttk.Label(self.control_frame, text="Scenario Level:", style="TLabel").grid(row=0, column=0, padx=(0, 5))
        self.level_var = tk.StringVar(value="1")
        self.level_dropdown = ttk.Combobox(self.control_frame, textvariable=self.level_var, 
                                          values=[str(i) for i in range(0, 8)], width=5, state="readonly")
        self.level_dropdown.grid(row=0, column=1, padx=(0, 20))
        self.level_dropdown.bind("<<ComboboxSelected>>", self.update_all_enemies)
        
        # Add enemy button
        self.add_btn = ttk.Button(self.control_frame, text="Add Enemy", command=self.show_enemy_selection)
        self.add_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Remove enemy button
        self.remove_btn = ttk.Button(self.control_frame, text="Remove Enemy", command=self.show_remove_selection)
        self.remove_btn.grid(row=0, column=3)
        
        # Create table frame
        self.table_frame = ttk.LabelFrame(self.main_frame, text="Enemy Statistics", padding="5")
        self.table_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.table_frame.columnconfigure(6, weight=1)  # Give more space to special traits
        
        # Create cards frame
        self.cards_frame = ttk.LabelFrame(self.main_frame, text="Enemy Cards & Initiatives", padding="5")
        self.cards_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        self.cards_frame.columnconfigure(0, weight=1)
        self.cards_frame.rowconfigure(0, weight=1)
        
        # Define all available enemies with explicit values for each level (0-7)
        self.all_enemies = {
            "Ancient Artillery": {
                "is_boss": False,
                "health": [4, 6, 7, 8, 9, 11, 14, 16],  # Levels 0-7
                "elite_health": [7, 9, 11, 13, 13, 15, 16, 20],
                "move": [0, 0, 0, 0, 0, 0, 0, 0],
                "elite_move": [0, 0, 0, 0, 0, 0, 0, 0],
                "attack": [2, 2, 2, 3, 4, 4, 4, 4],
                "elite_attack": [3, 3, 3, 4, 4, 4, 5, 5],
                "range": [4, 4, 5, 5, 5, 6, 6, 7],
                "elite_range": [5, 5, 6, 7, 6, 7, 7, 7],
                "traits": "",
                "elite_traits": "",
                "conditional_traits": {
                    "elite": {
                        "levels": [4, 5, 6, 7],  # Levels where additional traits apply
                        "traits": "Target 2"  # Additional traits for these levels
                    }
                },
                "cards": [
                    {"name": "PUSH 2, Target all adjacent enemies - ATTACK {attack-2}, SHIELD 2", "initiative": "17"},
                    {"name": "PUSH 1, Target all adjacent enemies - ATTACK {attack-1} at RANGE {range-1}, Targeting 3 tiles", "initiative": "37"},
                    {"name": "PUSH 1, Target all adjacent enemies - ATTACK {attack-1} at RANGE {range-1}, Targeting 7 tiles", "initiative": "37"},
                    {"name": "ATTACK {attack-1} at RANGE {range+2}", "initiative": "46"},
                    {"name": "ATTACK {attack-1} Targeting 3 enemies, IMMOBOLIZE", "initiative": "46"},
                    {"name": "ATTACK {attack}, All adjacent enemies suffer 2 damage. Redraw", "initiative": "71"},
                    {"name": "ATTACK {attack}, All adjacent enemies suffer 2 damage. Redraw", "initiative": "71"},
                    {"name": "ATTACK {attack+1}", "initiative": "95"}
                ]
            },
            "Bandit Archer": {
                "is_boss": False,  # Regular enemy
                "health": [4, 5, 6, 6, 8, 10, 10, 13],
                "elite_health": [6, 7, 8, 9, 10, 12, 13, 17],
                "move": [2, 2, 3, 3, 3, 3, 4, 4],
                "elite_move": [2, 3, 3, 3, 3, 4, 4, 4],
                "attack": [2, 2, 2, 3, 3, 3, 4, 4],
                "elite_attack": [3, 3, 3, 4, 4, 4, 4, 5],
                "range": [3, 4, 4, 4, 4, 5, 5, 5],
                "elite_range": [3, 5, 5, 5, 6, 6, 6, 6],
                "traits": "",
                "elite_traits": "",
                "conditional_traits": {
                    "elite": {
                        "levels": [4, 5, 6, 7],  # Levels where additional traits apply
                        "traits": "Poison"  # Additional traits for these levels
                    }
                },
                "cards": [
                    {"name": "MOVE {move-1}, ATTACK {attack-1}, Create a 3 damage trap in the hex closest to an enemy", "initiative": "14"},
                    {"name": "MOVE {move+1}, ATTACK {attack-1}", "initiative": "16"},
                    {"name": "MOVE {move}, ATTACK {attack-1} at RANGE {range+1}, IMMOBOLIZE, Redraw", "initiative": "29"},
                    {"name": "MOVE {move}, ATTACK {attack}", "initiative": "31"},
                    {"name": "MOVE {move}, ATTACK {attack+1} at RANGE {range-1}", "initiative": "32"},
                    {"name": "MOVE {move-1}, ATTACK {attack+1}", "initiative": "44"},
                    {"name": "Attack {attack-1} Target 2", "initiative": "56"},
                    {"name": "ATTACK {attack+1} at RANGE {range+1}, Redraw", "initiative": "68"}
                ]
            },
            "Bandit Commander": {
                "is_boss": True, 
                "health": ["8*C", "10*C", "12*C", "13*C", "15*C", "16*C", "19*C", "23*C"],  # Levels 0-7
                "elite_health": [10, 12, 14, 16, 18, 20, 22, 24],
                "move": [3, 3, 4, 4, 4, 5, 5, 5],
                "elite_move": [2, 2, 3, 3, 3, 4, 4, 4],
                "attack": [3, 3, 3, 4, 4, 5, 5, 5],
                "elite_attack": [3, 3, 4, 4, 5, 5, 6, 6],
                "range": [0, 0, 0, 0, 0, 0, 0, 0],
                "elite_range": [0, 0, 0, 0, 0, 0, 0, 0],
                "traits": "Immune to STUN, IMMOBOLIZE, CURSE",
                "elite_traits": "Shield 2, Retaliate 1",
                "conditional_traits": {},
                "cards": [
                    {"name": "Summon Living Bones", "initiative": "11"},
                    {"name": "Summon Living Bones", "initiative": "14"},
                    {"name": "Summon Living Bones, Redraw", "initiative": "17"},
                    {"name": "MOVE {move}, ATTACK {attack}", "initiative": "36"},
                    {"name": "MOVE {move-1}, ATTACK {attack-1} at RANGE 3, Target 2", "initiative": "52"},
                    {"name": "MOVE to next door and reveal room", "initiative": "73"},
                    {"name": "MOVE to next door and reveal room", "initiative": "79"},
                    {"name": "MOVE to next door and reveal room, Redraw", "initiative": "85"}
                ]
            },
            "Bandit Guard": {
                "is_boss": False,
                "health": [5, 6, 6, 9, 10, 11, 14, 16],
                "elite_health": [9, 9, 10, 10, 11, 12, 14, 14],
                "move": [2, 3, 3, 3, 4, 4, 4, 4],
                "elite_move": [2, 3, 3, 3, 3, 3, 3, 3],
                "attack": [2, 2, 3, 3, 3, 4, 4, 4],
                "elite_attack": [3, 3, 4, 4, 4, 5, 5, 5],
                "range": [0, 0, 0, 0, 0, 0, 0, 0],
                "elite_range": [0, 0, 0, 0, 0, 0, 0, 0],
                "traits": "",
                "elite_traits": "",
                "conditional_traits": {
                    "elite": [
                        {
                            "levels": [1, 2],
                            "traits": "Shield 1"
                        },
                        {
                            "levels": [3],
                            "traits": "Shield 2"
                        },
                        {
                            "levels": [4, 5, 6],
                            "traits": "Shield 2, MUDDLE"
                        },
                        {
                            "levels": [7],
                            "traits": "Shield 3, MUDDLE"
                        }
                    ]
                },
                "cards": [
                    {"name": "MOVE {move-1}, ATTACK {attack-1}, Create a 3 damage trap in the hex closest to an enemy", "initiative": "14"},
                    {"name": "MOVE {move+1}, ATTACK {attack-1}", "initiative": "16"},
                    {"name": "MOVE {move}, ATTACK {attack-1} at RANGE {range+1}, IMMOBOLIZE, Redraw", "initiative": "29"},
                    {"name": "MOVE {move}, ATTACK {attack}", "initiative": "31"},
                    {"name": "MOVE {move}, ATTACK {attack+1} at RANGE {range-1}", "initiative": "32"},
                    {"name": "MOVE {move-1}, ATTACK {attack+1}", "initiative": "44"},
                    {"name": "Attack {attack-1} Target 2", "initiative": "56"},
                    {"name": "ATTACK {attack+1} at RANGE {range+1}, Redraw", "initiative": "68"}
                ]
            },
            "Living Bones": {
                "health": [5, 6, 6, 7, 7, 8, 8, 9],
                "elite_health": [9, 10, 11, 12, 13, 14, 15, 16],
                "move": [2, 2, 2, 2, 3, 3, 3, 3],
                "elite_move": [2, 2, 3, 3, 3, 4, 4, 4],
                "attack": [1, 1, 2, 2, 2, 3, 3, 3],
                "elite_attack": [2, 2, 3, 3, 4, 4, 5, 5],
                "range": [0, 0, 0, 0, 0, 0, 0, 0],
                "elite_range": [0, 0, 0, 0, 0, 0, 0, 0],
                "traits": "Shield 1, Poison",
                "elite_traits": "Shield 2, Poison, Curse",
                "conditional_traits": {
                    "elite": {
                        "levels": [4, 5, 6, 7],  # Levels where additional traits apply
                        "traits": "Poison"  # Additional traits for these levels
                    }
                },
                "cards": [
                    {"name": "Attack {attack}", "initiative": "10"},
                    {"name": "Move {move} Attack {attack-1}", "initiative": "25"},
                    {"name": "Shield 1 Heal 1", "initiative": "45"},
                    {"name": "Poison Attack {attack-1}", "initiative": "15"},
                    {"name": "Move 1 Attack {attack+1}", "initiative": "35"},
                    {"name": "Shield 2", "initiative": "05"},
                    {"name": "Curse Attack {attack-1}", "initiative": "30"},
                    {"name": "Move {move+1}", "initiative": "55"}
                ]
            },
            "Cultist": {
                "health": [4, 5, 7, 9, 10, 11, 14, 15],
                "elite_health": [7, 9, 12, 13, 15, 18, 22, 25],
                "move": [2, 2, 2, 3, 3, 3, 3, 3],
                "elite_move": [2, 2, 2, 3, 3, 3, 3, 4],
                "attack": [1, 1, 1, 1, 2, 2, 2, 3],
                "elite_attack": [2, 2, 2, 2, 3, 3, 3, 4],
                "range": [0, 0, 0, 0, 0, 0, 0, 0],
                "elite_range": [0, 0, 0, 0, 0, 0, 0, 0],
                "traits": "Curse, Heal",
                "elite_traits": "Curse, Heal 2, Shield 1",
                "conditional_traits": {},
                "cards": [
                    {"name": "Attack {attack}", "initiative": "20"},
                    {"name": "Move {move} Heal 2", "initiative": "40"},
                    {"name": "Summon Living Bones", "initiative": "60"},
                    {"name": "Curse Attack {attack-1}", "initiative": "25"},
                    {"name": "Move 1 Heal 3", "initiative": "45"},
                    {"name": "Attack {attack+1}", "initiative": "15"},
                    {"name": "Shield 1 Curse", "initiative": "35"},
                    {"name": "Move {move+1}", "initiative": "50"}
                ]
            },
            "Hound": {
                "health": [5, 6, 6, 7, 7, 8, 8, 9],
                "elite_health": [9, 10, 11, 12, 13, 14, 15, 16],
                "move": [3, 3, 3, 4, 4, 4, 5, 5],
                "elite_move": [3, 3, 4, 4, 4, 5, 5, 5],
                "attack": [2, 2, 3, 3, 3, 4, 4, 4],
                "elite_attack": [3, 3, 4, 4, 5, 5, 6, 6],
                "range": [0, 0, 0, 0, 0, 0, 0, 0],
                "elite_range": [0, 0, 0, 0, 0, 0, 0, 0],
                "traits": "Jump, Wound",
                "elite_traits": "Jump, Wound, Poison",
                "conditional_traits": {},
                "cards": [
                    {"name": "Attack {attack}", "initiative": "15"},
                    {"name": "Move {move} Attack {attack-1}", "initiative": "30"},
                    {"name": "Jump Attack", "initiative": "50"},
                    {"name": "Wound Attack {attack-1}", "initiative": "20"},
                    {"name": "Move 2 Attack {attack}", "initiative": "40"},
                    {"name": "Poison Attack {attack-1}", "initiative": "10"},
                    {"name": "Jump Move {move+1}", "initiative": "35"},
                    {"name": "Attack {attack+1}", "initiative": "55"}
                ]
            }
        }
        
        # Currently displayed enemies
        self.displayed_enemies = []
        
        # Track which cards have been drawn
        self.drawn_cards = {}  # enemy_name -> list of booleans for each card
        
        # Create the table (initially empty)
        self.create_table_headers()
        
        # Add instructions
        instructions = ttk.Label(
            self.main_frame, 
            text="Select a scenario level to update all enemy statistics. Use 'Add Enemy' to select which enemies to display.",
            wraplength=800,
            style="TLabel"
        )
        instructions.grid(row=3, column=0, columnspan=2, pady=(10, 0))
    
    def create_table_headers(self):
        # Define columns with emojis only - increased width for Name and Level
        columns = [
            ("Name", "Name", 150),  # 50% wider for longer names
            ("Level", "Level", 60),  # 50% wider
            ("Health", "❤️", 40),
            ("Move", "🥾", 40),
            ("Attack", "⚔️", 40),
            ("Range", "🏹", 40),
            ("Special Traits", "Special", 200)
        ]
        
        # Create headers
        for col_idx, (col_id, col_name, width) in enumerate(columns):
            header = ttk.Label(self.table_frame, text=col_name, style="Header.TLabel", width=width//10)
            header.grid(row=0, column=col_idx, padx=2, pady=2, sticky=tk.W+tk.E)
            self.table_frame.columnconfigure(col_idx, weight=1 if col_id == "Special Traits" else 0)
    
    def get_traits_for_level(self, enemy_data, is_elite, current_level):
        """Get traits for a specific level, including conditional traits"""
        base_traits = enemy_data["elite_traits"] if is_elite else enemy_data["traits"]
        
        # Check for conditional traits
        if "conditional_traits" in enemy_data and enemy_data["conditional_traits"]:
            conditional_key = "elite" if is_elite else "normal"
            
            if conditional_key in enemy_data["conditional_traits"]:
                # Handle both old format (dict) and new format (list of dicts)
                conditional_data = enemy_data["conditional_traits"][conditional_key]
                
                # If it's a list of conditions (new format)
                if isinstance(conditional_data, list):
                    for condition in conditional_data:
                        if current_level in condition["levels"]:
                            # Add conditional traits to base traits
                            if base_traits:
                                return f"{base_traits}, {condition['traits']}"
                            else:
                                return condition["traits"]
                # If it's a single condition (old format)
                elif isinstance(conditional_data, dict):
                    if current_level in conditional_data["levels"]:
                        # Add conditional traits to base traits
                        if base_traits:
                            return f"{base_traits}, {conditional_data['traits']}"
                        else:
                            return conditional_data["traits"]
        
        return base_traits
    
    def show_enemy_selection(self):
        # Create a popup window for enemy selection
        popup = tk.Toplevel(self.root)
        popup.title("Select Enemy to Add")
        popup.geometry("300x200")  # Reduced height since we removed boss checkbox
        popup.transient(self.root)
        popup.grab_set()
        popup.configure(background=self.bg_color)
        
        ttk.Label(popup, text="Select an enemy to add:", style="TLabel").pack(pady=10)
        
        # Create dropdown with all enemies
        available_enemies = list(self.all_enemies.keys())
        
        if not available_enemies:
            ttk.Label(popup, text="No enemies available.", style="TLabel").pack(pady=10)
            ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
            return
            
        enemy_var = tk.StringVar()
        enemy_dropdown = ttk.Combobox(popup, textvariable=enemy_var, 
                                    values=available_enemies, state="readonly")
        enemy_dropdown.pack(pady=10)
        
        # Add elite option checkbox (hidden for bosses)
        elite_var = tk.BooleanVar()
        elite_check = ttk.Checkbutton(popup, text="Include Elite Version", variable=elite_var, style="TCheckbutton")
        elite_check.pack(pady=5)
        
        def update_checkboxes(*args):
            selected = enemy_var.get()
            if selected and selected in self.all_enemies:
                is_boss = self.all_enemies[selected].get("is_boss", False)
                if is_boss:
                    elite_check.pack_forget()  # Hide elite checkbox for bosses
                else:
                    elite_check.pack(pady=5)  # Show elite checkbox
        
        enemy_var.trace("w", update_checkboxes)
        
        def add_selected_enemy():
            selected = enemy_var.get()
            if selected:
                # Use the preset is_boss value from enemy data
                is_boss = self.all_enemies[selected].get("is_boss", False)
                self.add_enemy(selected, elite_var.get(), is_boss)
                popup.destroy()
        
        ttk.Button(popup, text="Add", command=add_selected_enemy).pack(pady=5)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=5)
        
        # Initial update of checkboxes
        if enemy_var.get():
            update_checkboxes()
        
    def show_remove_selection(self):
        if not self.displayed_enemies:
            messagebox.showinfo("Info", "No enemies to remove.")
            return
            
        # Create a popup window for enemy removal
        popup = tk.Toplevel(self.root)
        popup.title("Select Enemy to Remove")
        popup.geometry("300x250")
        popup.transient(self.root)
        popup.grab_set()
        popup.configure(background=self.bg_color)
        
        ttk.Label(popup, text="Select an enemy to remove:", style="TLabel").pack(pady=10)
        
        # Create dropdown with displayed enemies
        displayed_enemy_names = [enemy["name"] for enemy in self.displayed_enemies]
        
        enemy_var = tk.StringVar()
        enemy_dropdown = ttk.Combobox(popup, textvariable=enemy_var, 
                                     values=displayed_enemy_names, state="readonly")
        enemy_dropdown.pack(pady=10)
        
        def remove_selected_enemy():
            selected = enemy_var.get()
            if selected:
                self.remove_enemy(selected)
                popup.destroy()
        
        ttk.Button(popup, text="Remove", command=remove_selected_enemy).pack(pady=5)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=5)
    
    def remove_enemy(self, enemy_name):
        # Remove the enemy from displayed enemies
        self.displayed_enemies = [enemy for enemy in self.displayed_enemies if enemy["name"] != enemy_name]
        
        # Remove from drawn cards tracking
        if enemy_name in self.drawn_cards:
            del self.drawn_cards[enemy_name]
        
        # Update the display
        self.update_display()
    
    def add_enemy(self, enemy_name, include_elite, is_boss=False):
        # Get the enemy data
        enemy_data = self.all_enemies[enemy_name]
        current_level = int(self.level_var.get())
        
        # For boss enemies, ignore the elite flag
        if is_boss:
            include_elite = False
        
        # Get stats for current level
        health = enemy_data["health"][current_level]
        move = enemy_data["move"][current_level]
        attack = enemy_data["attack"][current_level]
        range_val = enemy_data["range"][current_level]
        
        # Get traits for current level
        traits = self.get_traits_for_level(enemy_data, False, current_level)
        
        # Determine display name and background color
        if is_boss:
            display_name = f"{enemy_name} (Boss)"
            bg_color = self.boss_color
        else:
            display_name = enemy_name
            bg_color = self.normal_color
        
        # Add normal/boss version to displayed enemies
        self.displayed_enemies.append({
            "name": display_name,
            "level": str(current_level),
            "health": str(health),
            "move": str(move),
            "attack": str(attack),
            "range": str(range_val),
            "traits": traits,
            "cards": enemy_data["cards"],
            "is_elite": False,
            "is_boss": is_boss,
            "base_name": enemy_name  # Store the base name for lookup
        })
        
        # Initialize drawn cards for this enemy
        self.drawn_cards[display_name] = [False] * 8
        
        # Add elite version if requested (and not a boss)
        if include_elite and not is_boss:
            elite_health = enemy_data["elite_health"][current_level]
            elite_move = enemy_data["elite_move"][current_level]
            elite_attack = enemy_data["elite_attack"][current_level]
            elite_range = enemy_data["elite_range"][current_level]
            
            # Get traits for current level (elite version)
            elite_traits = self.get_traits_for_level(enemy_data, True, current_level)
            
            elite_name = f"{enemy_name} (Elite)"
            
            self.displayed_enemies.append({
                "name": elite_name,
                "level": str(current_level),
                "health": str(elite_health),
                "move": str(elite_move),
                "attack": str(elite_attack),
                "range": str(elite_range),
                "traits": elite_traits,
                "cards": enemy_data["cards"],
                "is_elite": True,
                "is_boss": False,
                "base_name": enemy_name  # Store the base name for lookup
            })
            
            # Initialize drawn cards for elite version
            self.drawn_cards[elite_name] = [False] * 8
        
        # Update the display
        self.update_display()
    
    def update_display(self):
        # Clear the table and cards display
        for widget in self.table_frame.winfo_children():
            if widget.grid_info()["row"] > 0:  # Keep headers
                widget.destroy()
        
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        # Recreate the table with current enemies
        self.create_table()
        
        # Recreate cards display
        self.create_cards_display()
    
    def create_table(self):
        # Define columns with widths - increased width for Name and Level
        columns = [
            ("Name", "Name", 200), 
            ("Level", "Level", 60),  
            ("Health", "❤️", 40),
            ("Move", "🥾", 40),
            ("Attack", "⚔️", 40),
            ("Range", "🏹", 40),
            ("Special Traits", "Special", 200)
        ]
        
        # Create table rows
        for row_idx, enemy in enumerate(self.displayed_enemies, start=1):
            for col_idx, (col_id, col_name, width) in enumerate(columns):
                # Get the correct key name for the enemy dictionary
                if col_id == "Special Traits":
                    key = "traits"
                else:
                    key = col_id.lower().replace(" ", "_")
                
                value = enemy[key]
                
                # Use different background based on enemy type
                if enemy.get("is_boss", False):
                    bg_color = self.boss_color  # Dark blue for bosses
                elif enemy["is_elite"]:
                    bg_color = self.elite_color  # Gold for elites
                else:
                    bg_color = self.normal_color  # Gray for normal
                
                cell_frame = tk.Frame(self.table_frame, bg=bg_color, relief="raised", borderwidth=1)
                cell_frame.grid(row=row_idx, column=col_idx, padx=2, pady=1, sticky=tk.W+tk.E)
                
                if col_id == "Special Traits":
                    # Special handling for traits with more space
                    label = tk.Label(cell_frame, text=value, wraplength=300, bg=bg_color, 
                                    fg=self.text_color, justify=tk.LEFT)
                    label.grid(sticky=tk.W+tk.E, padx=2, pady=2)
                else:
                    label = tk.Label(cell_frame, text=value, bg=bg_color, fg=self.text_color, width=width//10)
                    label.grid(sticky=tk.W+tk.E, padx=2, pady=2)
        
    def create_cards_display(self):
        if not self.displayed_enemies:
            return
            
        # Create a notebook for enemy cards
        self.cards_notebook = ttk.Notebook(self.cards_frame)
        self.cards_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs for each enemy
        for enemy in self.displayed_enemies:
            frame = ttk.Frame(self.cards_notebook, padding="5")
            self.cards_notebook.add(frame, text=enemy["name"])
            
            # Create cards display for this enemy
            self.create_enemy_cards_display(frame, enemy)
    
    def create_enemy_cards_display(self, parent, enemy):
        # Create initiatives frame (on the left) - make it narrower
        initiatives_frame = ttk.LabelFrame(parent, text="Initiatives")
        initiatives_frame.grid(row=0, column=0, padx=3, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create a frame for cards (in the middle)
        cards_frame = ttk.LabelFrame(parent, text="Ability Cards")
        cards_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create a frame for drawn checkboxes (on the right)
        drawn_frame = ttk.LabelFrame(parent, text="Drawn")
        drawn_frame.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights to make initiatives frame narrower
        parent.columnconfigure(0, weight=1)   # Initiatives - minimal space
        parent.columnconfigure(1, weight=6)   # Cards - most space
        parent.columnconfigure(2, weight=1)   # Drawn - minimal space
        parent.rowconfigure(0, weight=1)
        
        # Sort cards by initiative (lowest first)
        sorted_cards = sorted(enemy["cards"], key=lambda x: int(x["initiative"]))
        
        # Store card frames and labels for later reference
        card_frames = []
        card_labels = []
        
        # Add initiatives (8 cards) - sorted with lowest at top
        for i, card in enumerate(sorted_cards):
            # Create a frame for each initiative to control height and background
            init_frame = tk.Frame(initiatives_frame, bg=self.card_bg, relief="raised", borderwidth=1, height=30, width=40)
            init_frame.grid(row=i, column=0, padx=2, pady=2, sticky=(tk.W, tk.E, tk.N, tk.S))
            init_frame.grid_propagate(False)  # Prevent frame from resizing to content
            initiatives_frame.columnconfigure(0, weight=1, minsize=40)  # Set minimum width
            initiatives_frame.rowconfigure(i, weight=1)
            
            # Center the initiative number in the frame
            init_label = tk.Label(init_frame, text=f"{card['initiative']}", 
                                foreground=self.text_color, background=self.card_bg,
                                font=("Arial", 10))
            init_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the label
        
        # Add cards (8 cards) - in same sorted order
        for i, card in enumerate(sorted_cards):
            # Calculate card values based on enemy stats
            card_text = self.calculate_card_text(card["name"], enemy)
            
            # Create card frame with fixed height
            card_frame = tk.Frame(cards_frame, bg=self.card_bg, relief="raised", borderwidth=1, height=30)
            card_frame.grid(row=i, column=0, padx=2, pady=2, sticky=(tk.W, tk.E, tk.N, tk.S))
            card_frame.grid_propagate(False)  # Prevent frame from resizing to content
            cards_frame.columnconfigure(0, weight=1)
            cards_frame.rowconfigure(i, weight=1)
            
            card_label = tk.Label(card_frame, text=card_text, wraplength=450, 
                                foreground=self.text_color, background=self.card_bg, 
                                justify=tk.LEFT, font=("Arial", 9))
            card_label.place(relx=0, rely=0.5, anchor="w")  # Left align, vertically center
            
            # Store for later reference
            card_frames.append(card_frame)
            card_labels.append(card_label)
        
        # Add drawn checkboxes (8 checkboxes) - in same sorted order
        enemy_name = enemy["name"]
        if enemy_name not in self.drawn_cards:
            self.drawn_cards[enemy_name] = [False] * 8
            
        for i, card in enumerate(sorted_cards):
            # Create a frame for each checkbox to control the background and height
            checkbox_frame = tk.Frame(drawn_frame, bg=self.card_bg, height=30, width=40)
            checkbox_frame.grid(row=i, column=0, padx=5, pady=2, sticky=(tk.W, tk.E, tk.N, tk.S))
            checkbox_frame.grid_propagate(False)  # Prevent frame from resizing to content
            drawn_frame.columnconfigure(0, weight=1, minsize=40)  # Set minimum width
            drawn_frame.rowconfigure(i, weight=1)
            
            drawn_var = tk.BooleanVar(value=self.drawn_cards[enemy_name][i])
            
            def make_toggle_callback(name, index, frame, label):
                return lambda: self.toggle_card_drawn(name, index, frame, label)
            
            # Use tk.Checkbutton with proper sizing - make it visible
            drawn_check = tk.Checkbutton(
                checkbox_frame, 
                variable=drawn_var,
                command=make_toggle_callback(enemy_name, i, card_frames[i], card_labels[i]),
                bg=self.card_bg,  # Set background color
                activebackground=self.card_bg,  # Set background when active
            )
            drawn_check.pack(expand=True)  # Use pack to center the checkbox
            
            # Update the card background based on initial state
            if self.drawn_cards[enemy_name][i]:
                card_frames[i].configure(bg="#a0a0a0")
                card_labels[i].configure(bg="#a0a0a0")
            
            # Store the variable for later access
            if not hasattr(self, 'drawn_vars'):
                self.drawn_vars = {}
            self.drawn_vars[f"{enemy_name}_{i}"] = drawn_var
    
    def toggle_card_drawn(self, enemy_name, card_index, card_frame, card_label):
        # Toggle the drawn status of the card
        self.drawn_cards[enemy_name][card_index] = not self.drawn_cards[enemy_name][card_index]
        
        # Update the card background color
        if self.drawn_cards[enemy_name][card_index]:
            card_frame.configure(bg="#a0a0a0")  # Grey background
            card_label.configure(bg="#a0a0a0")  # Grey background
        else:
            card_frame.configure(bg=self.card_bg)  # Original background
            card_label.configure(bg=self.card_bg)  # Original background
    
    def calculate_card_text(self, card_template, enemy):
        """Replace placeholders in card text with actual values from enemy stats"""
        try:
            # Get enemy stats as integers
            attack = int(enemy["attack"])
            move = int(enemy["move"])
            range_val = int(enemy["range"])
            
            # Evaluate expressions in the card template
            card_text = card_template
            
            # Handle {attack} placeholders with modifiers
            if "{attack" in card_text:
                import re
                # Find all attack expressions like {attack}, {attack+1}, {attack-1}
                attack_exprs = re.findall(r'\{attack([+-]\d+)?\}', card_text)
                for expr in attack_exprs:
                    if expr:
                        # Calculate modified attack value
                        modifier = int(expr)
                        value = max(0, attack + modifier)  # Ensure non-negative
                        card_text = card_text.replace(f"{{attack{expr}}}", str(value))
                    else:
                        card_text = card_text.replace("{attack}", str(attack))
            
            # Handle {move} placeholders with modifiers
            if "{move" in card_text:
                import re
                move_exprs = re.findall(r'\{move([+-]\d+)?\}', card_text)
                for expr in move_exprs:
                    if expr:
                        modifier = int(expr)
                        value = max(0, move + modifier)  # Ensure non-negative
                        card_text = card_text.replace(f"{{move{expr}}}", str(value))
                    else:
                        card_text = card_text.replace("{move}", str(move))
            
            # Handle {range} placeholders
            if "{range" in card_text:
                import re
                range_exprs = re.findall(r'\{range([+-]\d+)?\}', card_text)
                for expr in range_exprs:
                    if expr:
                        modifier = int(expr)
                        value = max(0, range_val + modifier)  # Ensure non-negative
                        card_text = card_text.replace(f"{{range{expr}}}", str(value))
                    else:
                        card_text = card_text.replace("{range}", str(range_val))
            
            return card_text
        except:
            return card_template  # Return original if any error occurs
    
    def update_all_enemies(self, event=None):
        # Update all displayed enemies with the new level
        current_level = int(self.level_var.get())
        
        for enemy in self.displayed_enemies:
            enemy_name = enemy["base_name"]  # Use the base name for lookup
            enemy_data = self.all_enemies[enemy_name]
            
            # Get stats based on level and elite status
            if enemy["is_elite"]:
                health = enemy_data["elite_health"][current_level]
                move = enemy_data["elite_move"][current_level]
                attack = enemy_data["elite_attack"][current_level]
                range_val = enemy_data["elite_range"][current_level]
            else:
                health = enemy_data["health"][current_level]
                move = enemy_data["move"][current_level]
                attack = enemy_data["attack"][current_level]
                range_val = enemy_data["range"][current_level]
            
            # Get traits for current level
            traits = self.get_traits_for_level(enemy_data, enemy["is_elite"], current_level)
            
            # Update enemy data
            enemy["level"] = str(current_level)
            enemy["health"] = str(health)
            enemy["move"] = str(move)
            enemy["attack"] = str(attack)
            enemy["range"] = str(range_val)
            enemy["traits"] = traits
        
        # Update the display
        self.update_display()

def main():
    root = tk.Tk()
    app = GloomhavenEnemyManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()