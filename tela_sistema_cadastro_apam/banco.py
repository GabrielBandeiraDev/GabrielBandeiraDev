import sqlite3
import pandas as pd
from tkinter import messagebox


class RegistrationSystem:
    def __init__(self):
        self.conn = sqlite3.connect('bancoAPAM.db')
        self.c = self.conn.cursor()
        self.create_tables()


    def get_columns(self, table: str='bancoapam'):
        self.c.execute(f"PRAGMA table_info({table})")
        db = self.c.fetchall()
        colunas = []
        for coluna_db in db:
            colunas.append(coluna_db[1])
        self.conn.commit()
        return colunas


# Corrigir tipagem de dados
    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS bancoapam
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            cpf TEXT,
                            matricula TEXT NOT NULL,
                            email TEXT NOT NULL,
                            telefone TEXT NOT NULL,
                            sexo TEXT NOT NULL,
                            data DATE NOT NULL,
                            endereco TEXT NOT NULL,
                            temperamento TEXT NOT NULL,
                            imagem TEXT NOT NULL)''')
        self.conn.commit()


        self.c.execute('''CREATE TABLE IF NOT EXISTS animal
                            (id_animal INTEGER PRIMARY KEY AUTOINCREMENT,
                            name_animal TEXT NOT NULL,
                            data_cadastro DATE NOT NULL,
                            especie TEXT NOT NULL,
                            genero TEXT NOT NULL,
                            idade_anos INTEGER,
                            idade_meses INTEGER,
                            porte TEXT NOT NULL,
                            pelagem TEXT NOT NULL,
                            raca TEXT NOT NULL)''')
        self.conn.commit()


        self.c.execute('''CREATE TABLE IF NOT EXISTS resgate
                            (id_resgate INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_animal INTEGER,
                            local_resgate TEXT NOT NULL,
                            atendimento TEXT NOT NULL,
                            necessario_intervencao_cirurgica TEXT NOT NULL,
                            destinacao_do_protegido TEXT NOT NULL,
                            historico_anamnese TEXT NOT NULL,
                            diagnostico_estado_saude TEXT NOT NULL,
                            tratamento_intervencao_e_medicacao TEXT NOT NULL,
                            data_resgate DATE NOT NULL,
                            castrado TEXT NOT NULL,
                            data_castracao DATE NOT NULL,
                            obito TEXT NOT NULL,
                            status_atual TEXT NOT NULL,
                            FOREIGN KEY (id_animal) REFERENCES animal(id_animal))''')
        self.conn.commit()


        self.c.execute('''CREATE TABLE IF NOT EXISTS observacoes
                            (id_obs INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_animal INTEGER,
                            data DATE NOT NULL,
                            observacao TEXT NOT NULL,
                            FOREIGN KEY (id_animal) REFERENCES animal(id_animal))''')
        self.conn.commit()


        self.c.execute('''CREATE TABLE IF NOT EXISTS vacinas
                            (id_vacinas INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_animal INTEGER,
                            data_vacina DATE NOT NULL,
                            peso REAL NOT NULL,
                            medicamento TEXT NOT NULL,
                            dose TEXT NOT NULL,
                            data_proxima_dose DATE NOT NULL,
                            FOREIGN KEY (id_animal) REFERENCES animal(id_animal))''')
        self.conn.commit()


        self.c.execute('''CREATE TABLE IF NOT EXISTS adocao
                            (id_adocao INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_animal INTEGER,
                            name_adotante TEXT NOT NULL,
                            rg TEXT NOT NULL,
                            cpf TEXT,
                            rua TEXT NOT NULL,
                            numero_rua TEXT NOT NULL,
                            complemento TEXT NOT NULL,
                            cep TEXT NOT NULL,
                            bairro TEXT NOT NULL,
                            cidade TEXT NOT NULL,
                            uf TEXT NOT NULL,
                            profissao TEXT NOT NULL,
                            email TEXT NOT NULL,
                            telefone_fixo TEXT NOT NULL,
                            celular TEXT NOT NULL,
                            referencia_rua TEXT NOT NULL,
                            data_adocao DATE NOT NULL,
                            FOREIGN KEY (id_animal) REFERENCES animal(id_animal))''')
        self.conn.commit()


    def register_apam(self, values_table: list, table: str='bancoapam'):
        colunas = self.get_columns(table=table)
        inter = ['?'] * len(colunas)  # Lista de valores para serem inseridos na consulta
        query = f"INSERT INTO {table}({', '.join(colunas)}) VALUES ({','.join(inter)})"
        self.c.execute(query, tuple(values_table))
        self.conn.commit()


        # Mostrando mesnsagem de sucesso
        messagebox.showinfo('Sucesso', 'Registrado com Sucesso!')
        print("Registrado com Sucesso!")


    def view_all_bancoapam(self, table: str='bancoapam'):
        self.c.execute(f"SELECT * FROM {table}")
        data = self.c.fetchall()
        return data


    def search_apam(self, id, table: str='bancoapam'):
        self.c.execute(f"SELECT * FROM {table} WHERE id=?", (id,))
        data = self.c.fetchone()
        if data:
            return data
        else:
            messagebox.showerror('Erro', f'Nenhum ID {id} encontrado!')


    def update_apam(self, valor_atualizado, table: str='bancoapam'):
        data = valor_atualizado
        colunas = self.get_columns(table=table)
        if data:
            query = f"UPDATE {table} SET name=?, cpf=?, data=?, email=?, endereco=?, matricula=?, telefone=?, sexo=?, temperamento=?, imagem=? WHERE id=?"  # Corrigir parâmetros
            self.c.execute(query,valor_atualizado)
            self.conn.commit()
            messagebox.showinfo('Sucesso', f'Informação do ID {valor_atualizado[10]} foi atualizado!')
        else:
            messagebox.showerror('Erro', f"Nenhum ID {valor_atualizado[10]} encontrado!")
            print(f"Nenhum ID '{valor_atualizado[10]}' encontrado!")


    def delete_apam(self, id, table: str='bancoapam'):
        self.c.execute(f"SELECT * FROM {table} WHERE id=?", (id,))
        data = self.c.fetchone()
        if data:
            self.c.execute(f"DELETE FROM {table} WHERE id=?", (id,))
            self.conn.commit()
            messagebox.showinfo('Sucesso', f"Informação do ID {id} foi deletado!")
            print(f"Informação do ID '{id}' foi deletado!")
        else:
            messagebox.showerror('Erro', f"Nenhum ID {id} encontrado!")
            print(f"Nenhum ID '{id}' encontrado!")


    def export_to_excel(self, table: str):
        self.c.execute(f"SELECT *, oid FROM {table}")
        to_excel = self.c.fetchall()
        colunas = self.get_columns(table=table)
        to_excel = pd.DataFrame(to_excel, columns=colunas)
        to_excel.to_excel(f'{table}.xlsx')
        self.conn.commit()


# create a registration system instance
registration_system = RegistrationSystem()
