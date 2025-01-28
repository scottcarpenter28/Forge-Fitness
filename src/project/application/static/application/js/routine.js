import ProgressBar from "./progress_bar.js";


class Timer{
   timer_container = null;
   current_time_span = null;
   current_time = 0;
   time_text = "00:00"
   current_exercise_span = null;
   exercise_text = ""
   time_interval = null;
   __current_timer = null;
   __is_paused = false;
   __count_direction = null;

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

      if(this.exercise_text.toLowerCase()==="rest")
         this.__set_timer_rest()
      else
         this.__set_timer_active();

   }

   set_time(time){
      this.current_time = time;
      this.set_time_text()
   }

   __to_time_str(){
      const minutes = Math.floor(this.current_time / 60);
      const seconds = this.current_time % 60;
      if(minutes == 0 && seconds == 0)
         return ""

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

   async start_count_down(time) {
      this.set_time(time);
      this.__count_direction = "DOWN";
      this.__current_timer = new Promise((resolve) => {
         const tick = () => {
            if (this.current_time <= 0) {
               // Play the final beep when countdown reaches 0
               window.start_beep_audio.currentTime = 0; // Reset to start of audio
               window.start_beep_audio.play();
               clearInterval(this.time_interval);
               resolve();
            } else if (this.current_time >= 1 && this.current_time <= 5) {
               // Ensure short beep plays every second consistently
               window.short_beep_audio.currentTime = 0; // Reset to start of audio
               window.short_beep_audio.play();
            }

            this.set_time_text();
            this.current_time--;
         };

         tick(); // Call immediately to handle the first tick
         this.time_interval = setInterval(tick, 1000); // Call every 1 second
      });
      return this.__current_timer;
   }



   start_count_up(){
      this.set_time(this.current_time);
      this.__count_direction = "UP"
      this.__current_timer = new Promise((resolve) => {
         const tick = () => {
            this.set_time_text();
            this.current_time++;
         };
         if(this.__is_paused){
            clearInterval(this.time_interval);
            resolve();
         }
         tick();
         this.time_interval = setInterval(tick, 1000);
      });
      return this.__current_timer
   }

   __pause(){
      if(this.time_interval)
         clearInterval(this.time_interval);
      this.__is_paused = true;
      return this.current_time;
   }

   __unpause(time_remaining){
      this.__is_paused = false;
      if(this.__count_direction === "DOWN")
         return this.start_count_down(time_remaining);
      else
         return this.start_count_up(time_remaining);
   }

   async pause_for_rest(rest_time) {
      let current_time = this.__pause();
      let count_direction = this.__count_direction;
      let current_exercise = this.exercise_text;

      this.set_current_exercise("Rest");
      await this.start_count_down(rest_time);


      this.set_current_exercise(current_exercise);
      this.__count_direction = count_direction;
      this.current_time = current_time;
      return current_time;
   }

}


class Exercise{
   name = "";
   duration_seconds = 30;
   reps = 10;
   sets = 3
   next_exercise = null;
   constructor(name, duration_seconds= 0, reps= 0, sets= 0) {
      this.name = name;
      this.duration_seconds = duration_seconds;
      this.reps = reps;
      this.sets = sets;
   }
   
   set_next_exercise(next){
      this.next_exercise = next;
   }
   
}


async function get_routine() {
   try {
      const response = await $.get(`/api/routine/${window.routine_uuid}`);
      return response;
   } catch (error) {
      add_alert(ALERT_TYPES.ERROR, "An issue occurred while fetching the routine. Please refresh and try again.");
      return {};
   }
}

let progress_bar = null;
let timer = null;
let current_exercise;
let completed_exercise = 0;
let total_exercise = 0;

async function start(routine_req){
   let routine = await routine_req;
   let exercises = routine.exercises.map((exercise) => new Exercise(exercise.exercise, exercise.duration, exercise.reps, exercise.sets));
   total_exercise = exercises.length;

   current_exercise = exercises[0];
   let prev_exercise = current_exercise;
   while(exercises.length > 0){
      prev_exercise.set_next_exercise(exercises.shift());
      prev_exercise = prev_exercise.next_exercise;
   }
   $("#exercise-controls").show();
   $("#exercise-tracker").show();
   $("#start-exercise").hide();
   timer.set_current_exercise(current_exercise.name);

   if(window.routine_type == "Cardio"){
      completed_exercise = -1
      let start = new Exercise("Starting", 5);
      start.next_exercise = current_exercise;
      current_exercise = start;
      await run_cardio_routine();
   }
   else{
      update_strength_texts();
      timer.start_count_up();
   }

}

function next_strength(){
   completed_exercise ++;
   let completed_percent = parseInt((completed_exercise/total_exercise) * 100);
   // Todo: Add in rest time between sets and exercises
   progress_bar.set_width(completed_percent);
   if(current_exercise.next_exercise == null)
      routine_complete();
   else {
      current_exercise = current_exercise.next_exercise;
      timer.set_current_exercise(current_exercise.name);
      update_strength_texts();
   }
}

let completed_sets = -1;
window.update_sets_completed = async function (){
   completed_sets += 1;
   $("#strength-exercise-sets").text(`${completed_sets}/${current_exercise.sets}`);
   if(completed_sets < current_exercise.sets) {
      $("#set-increment-btn").prop( "disabled", true );

      if(completed_sets > 0) {
         await timer.pause_for_rest(window.set_rest_time);
         timer.start_count_up();
      }
      $("#set-increment-btn").prop( "disabled", false );
   }
   else {
      $("#set-increment-btn").prop( "disabled", true );
      await timer.pause_for_rest(window.exercise_rest_time);
      timer.start_count_up();
      next_strength();
   }

}


function update_strength_texts(){
   completed_sets = -1;
   $("#strength-exercise-name").text(current_exercise.name);
   $("#strength-exercise-reps").text(current_exercise.reps);
   update_sets_completed();
}

async function run_cardio_routine(){
   while(current_exercise !== null){
      timer.set_current_exercise(current_exercise.name);
      if(current_exercise.next_exercise != null)
         $("#next-exercise").text(current_exercise.next_exercise.name);
      else
         $("#next-exercise").text("");
      await timer.start_count_down(current_exercise.duration_seconds);
      update_cardio_progress();
   }
   routine_complete();
}

function update_cardio_progress(){
   completed_exercise ++;
   let completed_percent = parseInt((completed_exercise/total_exercise) * 100);
   progress_bar.set_width(completed_percent);
   current_exercise = current_exercise.next_exercise;
}

window.add_rest_time = async function(){
   let time_remaining = await timer.pause_for_rest(20);
   await timer.start_count_down(time_remaining);
   update_cardio_progress();
   await run_cardio_routine();
}

function routine_complete(){
   timer.set_current_exercise("Completed!")
   $("#exercise-controls").hide();
   $("#exercise-tracker").hide();
   $("#complete-exercise").show();
}


$(document).ready(function() {
   progress_bar = new ProgressBar("routine-progress");
   timer = new Timer("timer", "current-time", "exercise");
   const routine_request = get_routine();

   $("#start-exercise-btn").click(() => start(routine_request));

});