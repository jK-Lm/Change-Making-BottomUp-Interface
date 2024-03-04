"""Solves the Change-Making problem using the dynamic Bottom Up approach, and displays the results in a table.
Modify the last line of code to whatever value you want. By jK-Lm on GitHub. All rights reserved, credit appreciated."""
import tkinter as tk

def changemaking_dyn(system, total_amount):
    """Returns the lowest coin count to achieve the 'total_amount' price.

    IN: system (list): Integers list representing a money change system. It is heavily recommended to have 1 inside.
        total_amount (int): The amount that should be reached using values in the system.

    OUT: nb_used_coins (list): The minimal amount of coins used with the system from 0 to 'total_amount'.
         coins_max (list): The highest used coin value for each value from 0 to 'total_amount'.
         vals_list (list): Amount of each value to be used to obtain 'total_amount'. It is made out of dictionaries representing values from 0 to 'total_amount' and the amount of each coin value needed."""
    
    nb_used_coins, coins_max = [0]*(total_amount+1), [0]*(total_amount+1)
    vals_list = [{item: 0 for item in system} for _ in range(total_amount+1)]

    for num in range(total_amount+1):
        for coin in system:
            if coin <= num:
                coins_needed = nb_used_coins[num-coin]+1
                if nb_used_coins[num] == 0 or coins_needed <= nb_used_coins[num]:
                    nb_used_coins[num] = coins_needed
                    coins_max[num] = coin
                    vals_list[num] = vals_list[num-coin].copy()
                    vals_list[num][coin] += 1
                        
    return nb_used_coins, coins_max, vals_list

def changemaking_table(system, amount):
    """Display a table to describe the amount of used coins in the change-making problem solving."""
    system = sorted(system)
    coins_needed, highest_coin, vals = changemaking_dyn(system, amount)
    top = list(range(amount+1))

    len_x = len(system)+3
    len_y = len(top)+1

    root = tk.Tk()
    root.geometry("1280x720")
    root.title("Change-Making - Bottom Up dynamic approach")
    root.configure(bg='white')
    
    sum_final_result = [f"{vals[-1][key]} {'coin' if key < 1 else 'bill'}{'s' if vals[-1][key] > 1 else ''} of {key}{currency}" for key in vals[-1] if vals[-1][key] > 0]
    syst_values = ", ".join(str(coin) for coin in system[:-1]) + (' and ' if len(system) > 1 else '') + str(system[-1])
    final_amount = ", ".join(sum_final_result[:-1]) + (' and ' if len(sum_final_result) > 1 else '') + sum_final_result[-1]

    label_res = tk.Label(root, bg='white', font=("Gadugi", 14), anchor='nw', justify='left', text=f"Here is how to obtain {amount}{currency} with the following values: {syst_values}.\nAt least {coins_needed[-1]} coins/money bills are required to obtain {amount}{currency}.\nIt consists of {final_amount}.")
    label_res.pack(side=tk.TOP, fill=tk.X, pady=5)

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    xscrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview) # Made by a human... of course...
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    yscrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

    frame2 = tk.Frame(canvas)
    frame2.pack_propagate(False)
    canvas.create_window((0, 0), window=frame2, anchor='nw')

    sys_index, top_index, total_index, coin_index = 0, 0, -1, -1

    for i in range(len_x):
        for j in range(len_y):
            bg_col = 'white'
            
            if i == 0 and j == 0:
                the_text = ''
                
            elif i == 0:
                bg_col = '#E3E3E3'
                if top_index < len(top):
                    the_text = str(top[top_index])
                    top_index += 1
                    
            elif i == len_x - 2:
                bg_col = '#CBCBCB'
                if total_index < len(coins_needed):
                    the_text = coins_needed[total_index] if j != 0 else 'Total'
                    total_index += 1
                    
            elif i == len_x - 1:
                bg_col = '#CBCBCB'
                if coin_index < len(highest_coin):
                    the_text = highest_coin[coin_index] if j != 0 else 'High'
                    coin_index += 1
                    
            elif j == 0:
                bg_col = '#E3E3E3'
                if sys_index < len(system):
                    the_text = system[sys_index]
                    sys_index += 1
                    
            elif j < len(vals) + 1:
                the_text = vals[j - 1][system[i - 1]] if i - 1 < len(vals[j - 1]) else '0'

            tab = tk.Frame(frame2, width=45, bg=bg_col, height=30, highlightbackground="black", highlightthickness=1, bd=0)
            tab.grid(row=i, column=j)
            text = tk.Label(tab, bg=bg_col, text=the_text, font=("Gadugi", 11))
            text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def frame_update(_):
        """Updates scrollbars on window resize."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame2.bind("<Configure>", frame_update)

    root.mainloop()

currency = '$'
changemaking_table([1, 2, 5, 10], 23) # Do not use comprehension lists, it will break.