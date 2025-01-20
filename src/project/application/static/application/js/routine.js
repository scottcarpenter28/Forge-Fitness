import ProgressBar from "./progress_bar.js";


class Timer{
   timer_container = null;
   current_time_span = null;
   current_time = 0;
   time_text = "00:00"
   current_exercise_span = null;
   exercise_text = ""
   time_interval = null;

   constructor(timer_container_id, current_time_span_id, current_exercise_span_id){
      this.set_timer_container(timer_container_id);
      this.set_time_span(current_time_span_id);
      this.set_exercise_span(current_exercise_span_id);
   }

   set_timer_container(timer_container_id){
      if(timer_container_id[0] !== "#")
         timer_container_id = "#"+timer_container_id;
      this.timer_container = $(timer_container_id);
   }

   set_time_span(time_span_id){
      if(time_span_id[0] !== "#")
         time_span_id = "#"+time_span_id;
      this.current_time_span = $(time_span_id);
      this.set_time_text()
   }

   set_time_text(){
      this.time_text = this.__to_time_str();
      this.current_time_span.text(this.time_text);
   }

   set_exercise_span(exercise_id){
      if(exercise_id[0] !== "#")
         exercise_id = "#"+exercise_id;
      this.current_exercise_span = $(exercise_id);
   }

   set_current_exercise(exercise){
      this.exercise_text = exercise;
      this.current_exercise_span.text(exercise);
   }

   set_time(time){
      this.current_time = time;
      this.set_time_text()
   }

   __to_time_str(){
      const minutes = Math.floor(this.current_time / 60);
      const seconds = this.current_time % 60;

      let time_text = seconds;
      if(minutes > 0){
         time_text = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
      }
      return time_text;
   }

   __set_timer_active(){
      this.timer_container.removeClass("rest");
      this.timer_container.addClass("active");
   }

   __set_timer_rest(){
      this.timer_container.removeClass("active");
      this.timer_container.addClass("rest");
   }

   start_count_down(time){
      this.set_time(time);
      this.time_interval = setInterval(() => {
         if (this.current_time <= 0) {
            clearInterval(this.time_interval);
            this.__set_timer_rest();
         }
         else{
            this.__set_timer_active();
         }
         this.set_time_text();
         this.current_time--;
      }, 1000);
   }

   start_count_up(){
      {
         this.set_time(0);
         this.time_interval = setInterval(() => {
            this.__set_timer_active();
            this.set_time_text();
            this.current_time++;
         }, 1000);
      }
   }

}


$(document).ready(function() {
   const progress = new ProgressBar("routine-progress");
   const timer = new Timer("timer", "current-time", "exercise");
   // timer.start_count_down(10);
   // timer.start_count_up();
});