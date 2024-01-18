from LolDbEntry import LolDbEntry

class LolDb:
    def __init__(self, init=False, dbName='EmpDb.csv'):      
        self.dbName = dbName
        self.entries = []
        print('TODO: __init__')


    def fetch_champions(self):
        print('TODO: fetch_champinfo')
        tupleList = [(entry.title, entry.name, entry.role, entry.gender, entry.position) for entry in self.entries]
        #tupleList = [('123', 'Brian Baker', 'SW-Engineer', 'Male', 'On-Site'),
        #             ('124', 'Eileen Dover', 'SW-Engineer', 'Male', 'On-Site'),
        #             ('125', 'Ann Chovey', 'SW-Engineer', 'Male', 'On-Site')]
        return tupleList

    def insert_champion(self, title, name, role, gender, position):
        newEntry = LolDbEntry(title=title, name=name, role=role, gender=gender, position=position)
        self.entries.append(newEntry)
        print('TODO: add_champinfo')

    def delete_champion(self, title):
        for entry in self.entries:
            if entry.title == title:
                self.entries.remove(entry)
                break
        print('TODO: delete_champinfo')

    def update_champion(self, new_name, new_role, new_gender, new_position, title):
        for entry in self.entries:
            if entry.title == title:
                entry.name = new_name
                entry.role = new_role
                entry.gender = new_gender
                entry.position = new_position
                break
        print('TODO: update_champinfo')

    def export_csv(self):
        with open(self.dbName, "w") as filehandle:
            for entry in self.entries:
                filehandle.write(f"{entry.title},{entry.name},{entry.role},{entry.gender},{entry.position}\n")
        print('TODO: export_csv')

    def import_csv(self, file_path):
        """
        - imports database entries from a CSV file
        - CSV : Comma Separated Values
        - no return value
        """
        with open(file_path, "r") as filehandle:
            for line in filehandle:
                values = line.strip().split(',')
                if len(values) == 5:
                    self.insert_champion(*values)
        print('TODO: import_csv')

    def title_exists(self, title):
        """
        - returns True if an entry exists for the specified 'title'
        - else returns False
        """
        return any(entry.title == title for entry in self.entries)
