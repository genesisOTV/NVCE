var feedApp = new Vue({
    el: '#feed-app',
    
    data/*like context; send this data to the html*/: {
        items: [],
        sources: [],
        newLink: "",
        route: "sources"
    },

    methods: {
        api: function(endpoint, method, data) {
            var config = {
                method: method || 'GET',
                body: data !== undefined ? JSON.stringify(data) : null,
                headers: {
                    'content-type': 'application/json'
                }
            };

            return fetch(endpoint, config)
                    .then((response) => response.json())
                    .catch((error) => console.log(error));
        },

        reload: function() {
            this.getSources();
            this.getItems();
        },

        getSources: function() {
            this.api("/feed/sources/").then((sources) => {
                this.sources = sources;
            });
        },

        getItems: function() {
            this.api("/feed/items/").then((items) => {
                this.items = items;
            });
        },

        newSource: function() {
            this.api("/feed/sources/", "POST", { url: this.newLink }).then(() => {
                this.reload();
            });
        },

        deleteSource: function(id) {
            this.api("/feed/sources/" + id + "/", "DELETE").then(() => {
                this.reload();
            });
        },
       
        setRoute: function(route) {
            this.route = route;
        },

        setup: function() {
            var hash = window.location.hash;
        
            if(hash) {
                this.route = hash.slice(1);
            }
        
            this.reload();
        },        
    }
});
