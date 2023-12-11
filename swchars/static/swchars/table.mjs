import { Backend } from './backend.mjs';


class Table {

    constructor() {
        this.table = document.querySelector('.chars-table');
        this.tbody = this.table.children[1];
        this.backend = new Backend();
        this.keys = [
            'name', 'height', 'mass', 'hair_color', 'eye_color',
            'birth_year', 'gender', 'homeworld'
        ]
    }


    async displayData(data) {
        if (this.table.classList.contains('hidden')) {
            this.table.classList.remove('hidden');
        }
        for (let i = 0; i < data.results.length; i++) {
            const tr = this.createRow();
            for (let j = 0; j < this.keys.length; j++) {
                this.insertCell(tr, data.results[i], this.keys[j]);
            }
            this.tbody.append(tr);
        }

    }

    createRow() {
        const tr = document.createElement('tr');
        tr.classList.add(['text-gray-700']);
        return tr;
    }

    insertCell(tr, data, key) {
        const td = document.createElement('td');
        td.classList.add('border-b-2', 'p-4', 'dark:border-dark-5')
        if (key === 'homeworld') {
            new Promise((resolve, reject) => {
                this.backend.loadItem(data[key], resolve, reject)
            }).then(data => {
                td.innerHTML = data.name;
            })
        } else if (!Array.isArray(data[key])) {
            td.innerHTML = data[key];
        } 
        tr.append(td);
    }
}

export { Table }
