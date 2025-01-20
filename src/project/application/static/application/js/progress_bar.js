export default class ProgressBar {
    container_id = "";
    progress_bar_fill = null;
    progress_bar_span = null;


    /*
    * Sets the progress bar up.
    * container_id: The id of the progress bar.
    * width: The starting width of the progress bar.
     */
    constructor(container_id, width=undefined) {
        this.set_container_id(container_id);
        this.progress_bar_fill = $(`${this.container_id} .progress-bar-fill`);
        this.progress_bar_span = $(`${this.container_id} .progress-bar-fill span`);


        if(!width) {
            width = this.get_width();
        }

        this.set_width(width);
    }

    /*
    * Sets the container ID for the progress bar.
    * container_id: The progress bar to use. Adds "#" if it is not included.
     */
    set_container_id(container_id) {
        if(container_id[0] !== "#")
            container_id = "#" + container_id;
        this.container_id = container_id;
    }

    /*
    * Sets the current width of the progress bar, then updates the text within the span.
    * width: The width to set of the progress bar.
     */
    set_width(width = 0) {
        if(width > 100)
            throw new Error("Progress bar width must be a number between 0 and 100.")
        if(width < 0)
            throw new Error("Progress bar width must be a number between 0 and 100.")

        width = parseFloat(width)
        if(!Number.isFinite(width))
            throw new Error("Progress bar width must be a number between 0 and 100.")


        this.progress_bar_fill.attr("prog-width", width);
        this.progress_bar_fill.css("width", this.get_width() >= 1? `${this.get_width()}%`: "0");
        this.set_span_text()
    }

    /*
    * Gets the current width of the progress bar.
    * return: The current value of the progress bar.
     */
    get_width() {
        return parseFloat(this.progress_bar_fill.attr("prog-width"));
    }

    set_span_text(){
        this.progress_bar_span.text(this.get_width() >= 1 ? `${this.get_width()}%`: "");
    }

}