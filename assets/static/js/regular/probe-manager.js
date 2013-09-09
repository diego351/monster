var probes = {
    list: {},
    register: function(spec) {
        this.list[spec.name] = spec;
    },
    paint_all: function() {
        for (var key in this.list) {
            this.list[key].paint();
        }
    },
    start: function(interval) {
        /* 
         * start() is intended to be run after document load. 
         * (since probe inits need the chart divs ready and all that..)
         */
        for (var key in this.list) {
            console.log("Initializing:");
            console.log(this.list[key]);
            this.list[key].init();
        }

        this.paint_all();
        /* setInerval binds the called function to window by defaut, so.. */
        /* This is both ugly and beautiful, isn't it?. */
        this.timer = setInterval(
            (function(self) {
                return function() {
                    self.paint_all();
                }     
            })(this),
            interval
        );
    },
    stop: function() {
        clearInterval(this.timer);
    }
};
