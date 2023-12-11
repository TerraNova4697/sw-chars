import { Backend } from "./backend.mjs";
import { Table } from "./table.mjs";


class Dispatcher {
    constructor() {
        this.previousPage = null;
        this.nextPage = 1;
        this.loadingSpan = document.querySelector('.loading-span')
        this.loadSpan = document.querySelector('.load-span')
        this.loadButton = document.querySelector('.load-button');
        this.infoLoading = document.querySelector('.info-loading');
        this.infoDone = document.querySelector('.info-done');
        this.readyToLoadChars = false;
        this.loadButton.addEventListener('click', (event) => this.loadData(event));
        this.backend = new Backend();
        this.table = new Table();
    }

    loadData(event) {
        this.loadSpan.classList.add('hidden');
        this.loadingSpan.classList.remove('hidden');
        new Promise((resolve, reject) => {
            this.backend.loadChars(this.nextPage, resolve, reject)
        }).then(data => {
            this.hideButton();
            this.nextPage = data.next;
            this.previousPage = data.previousPage;
            this.table.displayData(data);
            this.observeIntersection();
        });
    }

    hideButton() {
        this.loadButton.classList.add('hidden');
    }

    observeIntersection() {
        const footer = document.querySelector('footer');

        this.readyToLoadChars = true;
        const obsOptions = {
            root: null,
            threshold: 0.1
        }

        const observer = new IntersectionObserver(this.obsCallback.bind(this), obsOptions);
        observer.observe(footer);
    }

    obsCallback(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting && this.readyToLoadChars && this.nextPage != null) {
                this.readyToLoadChars = false;
                this.infoLoading.classList.toggle('hidden')
                new Promise((resolve, reject) => {
                    this.backend.loadChars(this.nextPage, resolve, reject)
                }).then(data => {
                    this.table.displayData(data);
                    this.nextPage = data.next;
                    this.previousPage = data.previousPage;
                    this.readyToLoadChars = true;
                    this.infoLoading.classList.toggle('hidden')
                })
            } else if (this.nextPage === null) {
                this.infoLoading.classList.add('hidden')
                this.infoDone.classList.remove('hidden')
            }
        })
    }

}


export { Dispatcher }
