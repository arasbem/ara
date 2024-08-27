from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Carica il file Excel
file_path = "PERMUTE.xlsx"
df = pd.read_excel(file_path)

# Ottenere le intestazioni delle colonne
column_headers = df.columns.tolist()

# Converti i dati in liste di stringhe
data_col_a = df.iloc[:, 0].astype(str).tolist()
data_col_b = df.iloc[:, 1].astype(str).tolist()
data_col_c = df.iloc[:, 2].astype(str).tolist()
data_col_d = df.iloc[:, 3].astype(str).tolist()
data_col_e = df.iloc[:, 4].astype(str).tolist()  # Aggiunta della colonna E

def get_row_data(index):
    if 0 <= index < len(data_col_a):
        current_data_a = data_col_a[index]
        current_data_b = data_col_b[index]
        current_data_c = data_col_c[index]
        current_data_d = data_col_d[index]
        current_data_e = data_col_e[index]  # Aggiunta della colonna E

        return {
            "index": index + 1,
            "col_a": current_data_a,
            "col_b": current_data_b,
            "col_c": current_data_c,
            "col_d": current_data_d,
            "col_e": current_data_e  # Aggiunta della colonna E
        }
    return None

@app.route('/')
def index():
    row_number = request.args.get('row', type=int, default=1)
    row_data = get_row_data(row_number - 1)
    return render_template('index.html', row_data=row_data, total_rows=len(data_col_a), headers=column_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
