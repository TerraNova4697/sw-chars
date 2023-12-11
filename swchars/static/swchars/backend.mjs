class Backend {
    constructor() {
        this.itemsApi = document.querySelector('.items-url').getAttribute('data-items-url');
        this.charsApi = document.querySelector('.chars-url').getAttribute('data-chars-url');
        this.axios = window.axios;
    }

    loadChars(page, resolve, reject) {
        this.axios.get(this.charsApi + `?page=${page}`)
            .then(function(response) {
                resolve(response.data);
            })
    }

    loadItem(url, resolve, reject) {
        const apiParams = this.getItemParamsFromStr(url);
        this.axios.get(this.itemsApi + `?type=${apiParams[0]}&id=${apiParams[1]}`)
            .then(function(response) {
                resolve(response.data);
            })
    }

    getItemParamsFromStr(url) {
        const params = url.split('/');
        return [params[params.length-3], params[params.length-2]];
    }
}


export { Backend }
