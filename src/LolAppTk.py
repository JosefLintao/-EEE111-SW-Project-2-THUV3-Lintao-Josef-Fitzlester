from LolDb import LolDb
from LolGuiTk import LolGuiTk

def main():
    db = LolDb(init=False, dbName='EmpDb.csv')
    app = LolGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()