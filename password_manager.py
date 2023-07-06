# importing dependencies
import PySimpleGUI as sg
import string
import random
import json
import pyperclip

# function for generating passwords
chars = [x for x in string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation]

# passwords
with open('./saved_pass.json', 'r') as file:
    saved_pass = json.load(file) 

accs = list(saved_pass.keys())

# Add your new theme colors and settings
sg.LOOK_AND_FEEL_TABLE['manualTheme'] = {'BACKGROUND': '#27374D',
                                        'TEXT': '#DDE6ED',
                                        'INPUT': '#526D82',
                                        'TEXT_INPUT': '#DDE6ED',
                                        'SCROLL': '#99CC99',
                                        'BUTTON': ('#435B66', '#DDE6ED'),
                                        'PROGRESS': ('#D1826B', '#CC8019'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0, 
'PROGRESS_DEPTH': 0, }

sg.theme('manualTheme')

# layout
layout = [
    [
        sg.Push(), 
        sg.Image('./themeimg.png', key='-THEME_IMAGE-',
                         pad=((50, 50), (50, 50))), 
        sg.Push()
    ],
    [
        sg.Push(),
        sg.Text('Password Length'),
        sg.Input(16, key='-PASS_LEN-', size=(5, 1)),
        sg.Push()
    ],
    [
        sg.Text('Insert New Password', font=('Cursive', 14))
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Push(),
        sg.Column(
            [
                [sg.Text('Account', font='bold')],
                [sg.Text('Password', font='bold')]
            ]
        ), 
        sg.Column(
            [
                [sg.Input('', key='-PASSWORD_ACC-', size=(25, 1))],
                [sg.Input(key='-PASSWORD-', size=(25, 1))],
            ]
        ),
        sg.Column(
            [
                [sg.VPush(), sg.Button('Generate', key='-GEN_PASS-', pad=((5, 5), (5, 5)))]
            ]
        , vertical_alignment='bottom'),
        sg.Push()
    ],
    [
        sg.Push(),
        sg.Button('Save', key='-SAVE-', pad=((5, 5), (5, 5))),
        sg.Button('Cancel', key='-CANCEL_GEN-', pad=((5, 5), (5, 5))),
        sg.Push()
    ],
    [
        sg.Text('Edit Or See Password', font=('Cursive', 14))
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Push(),
        sg.Column(
            [
                [sg.Text('Account', font='bold')],
                [sg.Text('Password', font='bold')]
            ]
        ), 
        sg.Column(
            [
                [sg.Combo(accs, key='-EDIT_ACC-', size=(25, 1), enable_events=True, readonly=True)],
                [sg.Input(key='-EDIT_PASSWORD-', size=(25, 1))],
            ]
        ),
        sg.Column(
            [
                [sg.VPush(), sg.Button('Generate', key='-GEN_EDIT_PASS-', pad=((5, 5), (5, 5)))]
            ]
        , vertical_alignment='bottom'),
        sg.Push()
    ],
    [
        sg.Push(),
        sg.Button('Copy', key='-COPY-', pad=((5, 5), (5, 5))),
        sg.Button('Save', key='-SAVE_EDIT-', pad=((5, 5), (5, 5))),
        sg.Button('Cancel', key='-CANCEL_EDIT-', pad=((5, 5), (5, 5))),
        sg.Button('Delete', key='-DELETE-', pad=((5, 5), (5, 5)), button_color=('White', 'Red')),
        sg.Push()
    ],
]

# create the window
window = sg.Window('Password Manager', layout, size=(500, 600))

# main loop
while True:
    event, values = window.read()

    # breaking condition of the main loop
    if event == sg.WIN_CLOSED:
        break

    # generate password
    if event == '-GEN_PASS-':
        if values['-PASS_LEN-'] == '':
            sg.popup('Enter a password length')
        elif not values['-PASS_LEN-'].isdigit():
            sg.popup('Password must be integer')
        else:
            pass_len = int(values['-PASS_LEN-'])
            password = ''.join(random.sample(chars, pass_len))
            window['-PASSWORD-'].update(password)

    # generate password in edit
    if event == '-GEN_EDIT_PASS-':
        pass_len = int(values['-PASS_LEN-'])
        password = ''.join(random.sample(chars, pass_len))
        window['-EDIT_PASSWORD-'].update(password)

    # saving the password functionality
    if event == '-SAVE-':
        if values['-PASSWORD_ACC-'] != '' and values['-PASSWORD-'] != '':
            acc = values['-PASSWORD_ACC-']
            password = values['-PASSWORD-']
            
            with open('./saved_pass.json', 'r') as file:
                saved_pass = json.load(file)
            
            saved_pass[acc] = password

            with open('./saved_pass.json', 'w') as file:
                json.dump(saved_pass, file)

            sg.popup(f'Password for {acc} has been saved successfully')

            window['-PASSWORD_ACC-'].update('')
            window['-PASSWORD-'].update('')

            accs = list(saved_pass.keys())
            window['-EDIT_ACC-'].update(values=accs)
        else:
            sg.popup('Please insert account name and password first.')

    # cancel to generation
    if event == '-CANCEL_GEN-':
        window['-PASSWORD_ACC-'].update('')
        window['-PASSWORD-'].update('') 

    # changing the selected account to edit or see password
    if event == '-EDIT_ACC-':
        with open('./saved_pass.json', 'r') as file:
            saved_pass = json.load(file)
        
        selected_acc = values['-EDIT_ACC-']
        window['-EDIT_PASSWORD-'].update(saved_pass[selected_acc])

    # saving the edited password functionality
    if event == '-SAVE_EDIT-':
        if values['-EDIT_ACC-'] != '' and values['-EDIT_PASSWORD-'] != '':
            acc = values['-EDIT_ACC-']
            password = values['-EDIT_PASSWORD-']
            
            with open('./saved_pass.json', 'r') as file:
                saved_pass = json.load(file)
            
            saved_pass[acc] = password

            with open('./saved_pass.json', 'w') as file:
                json.dump(saved_pass, file)

            sg.popup(f'Saved the edits for {acc}, successfully')

            window['-EDIT_ACC-'].update('')
            window['-EDIT_PASSWORD-'].update('')

            accs = list(saved_pass.keys())
            window['-EDIT_ACC-'].update(values=accs) 
        else:
            sg.popup('Please insert account name and password first.')

    # cancel to edit
    if event == '-CANCEL_EDIT-':
        window['-EDIT_ACC-'].update('')
        window['-EDIT_PASSWORD-'].update('') 

    # delete an account password
    if event == '-DELETE-':
        if values['-EDIT_ACC-'] != '' and values['-EDIT_PASSWORD-'] != '':
            acc = values['-EDIT_ACC-']
            
            with open('./saved_pass.json', 'r') as file:
                saved_pass = json.load(file)
            
            saved_pass.pop(acc)

            with open('./saved_pass.json', 'w') as file:
                json.dump(saved_pass, file)

            sg.popup(f'Deleted Password for {acc}, successfully')

            window['-EDIT_ACC-'].update('')
            window['-EDIT_PASSWORD-'].update('')

            accs = list(saved_pass.keys())
            window['-EDIT_ACC-'].update(values=accs) 
        else:
            sg.popup('Please insert account name and password first.')

    # copy to clipboard functionality
    if event == '-COPY-':
        if values['-EDIT_ACC-'] != '' and values['-EDIT_PASSWORD-'] != '':
            pyperclip.copy(values['-EDIT_PASSWORD-'])
            sg.popup(f"Password for {values['-EDIT_ACC-']} has been copied to clipboard")
        else:
            sg.popup('Please insert account name and password first.')

window.close()