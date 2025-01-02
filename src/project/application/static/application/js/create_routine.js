class Exercise {
    constructor({ id, exercise, reps, sets, duration }) {
        this.id = `exercise_${id}`;
        this.exercise = exercise;
        this.reps = reps || 0;
        this.sets = sets || 0;
        this.duration = duration || 0;
    }

    set_exercise_id(id){
        this.id = `exercise_${id}`;
    }

    table_element() {
        return `
            <tr id="tr_${this.id}">
                <td>${this.exercise}</td>
                <td class="strength-routine-col">${this.reps || ''}</td>
                <td class="strength-routine-col">${this.sets || ''}</td>
                <td class="cardio-routine-col">${this.duration || ''}</td>
                <td>
                    <div class="routine-actions">
                        <div class="move-exercise-up">
                            <i class="fa-solid fa-angle-up"></i>
                        </div>
                        <div class="remove-exercise">
                            <i class="fa-solid fa-trash"></i>
                        </div>
                        <div class="move-exercise-down">
                            <i class="fa-solid fa-angle-down"></i>
                        </div>
                    </div>
                </td>
            </tr>
        `;
    }

    mobile_table_element() {
        return `
            <div id="mb_${this.id}" class="mobile-table-card">
                <span style="display: none">${this.id}</span>
                <span>Exercise: ${this.exercise}</span>
                <span class="strength-routine-col">Reps: ${this.reps || ''}</span>
                <span class="strength-routine-col">Sets: ${this.sets || ''}</span>
                <span class="cardio-routine-col">Time: ${this.duration || ''}</span>
                <div class="routine-actions">
                    <div class="move-exercise-up">
                        <i class="fa-solid fa-angle-up"></i>
                    </div>
                    <div class="remove-exercise">
                        <i class="fa-solid fa-trash"></i>
                    </div>
                    <div class="move-exercise-down">
                        <i class="fa-solid fa-angle-down"></i>
                    </div>
                </div>
            </div>
        `;
    }
}


$(document).ready(function() {
    $('#id_equipment').select2();
    $('#id_target_muscles').select2();

    const routine_select_box = $("#id_routine_type");

    const cardio_routine_div = $("#cardio-routine-creator");
    const cardio_col_selector = ".cardio-routine-col";

    const strength_col_selector = ".strength-routine-col";
    const strength_routine_div = $("#strength-routine-creator");

    /*
    * Updates the parts of the form being displayed based on the routine type selected.
     */
    function update_routine_display(){
        const current_routine = routine_select_box.val();
        if(current_routine.toLowerCase() === "strength"){
            cardio_routine_div.hide();
            $(cardio_col_selector).hide();

            strength_routine_div.fadeIn();
            $(strength_col_selector).show();
        }else{
            strength_routine_div.hide();
            $(strength_col_selector).hide();

            cardio_routine_div.fadeIn();
            $(cardio_col_selector).show();
        }
    }

    // Setup event listener, then check the update the form to match what was loaded in.
    routine_select_box.change(update_routine_display);
    update_routine_display();

    const add_cardio_btn = $("#add-cardio-exercise");
    const add_strength_btn = $("#add-strength-exercise");

    const cardio_exercise_name_input = $("#cardio-exercise");
    const strength_exercise_name_input = $("#strength-exercise");
    const cardio_exercise_duration_input = $("#cardio-duration");
    const num_reps_input = $("#num-reps");
    const num_sets_input = $("#num-sets")
    const set_rest_input = $("#set-rest");
    const between_exercise_rest_input = $("#exercise-rest");

    function add_exercise(exercise_name) {
        // const exercise_name = cardio_exercise_name_input.val();
        const exercise_duration = parseInt(cardio_exercise_duration_input.val());
        const num_reps = parseInt(num_reps_input.val());
        const num_sets = parseInt(num_sets_input.val());

        if (exercise_name === "") {
            add_alert(ALERT_TYPES.ERROR, "No name provided for exercise.");
            return;
        }
        if (!Number.isInteger(exercise_duration)) {
            add_alert(ALERT_TYPES.ERROR, "Exercise duration must be a number.");
            cardio_exercise_duration_input.val("30");
            return;
        }
        if (exercise_duration < 5) {
            add_alert(ALERT_TYPES.ERROR, "Exercise duration must be at least 5 seconds.");
            return;
        }
        if(!Number.isInteger(num_reps)) {
            add_alert(ALERT_TYPES.ERROR, "Exercise duration must be a number.");
            num_reps_input.val("10");
            return;
        }
        if(num_reps <= 0) {
            add_alert(ALERT_TYPES.ERROR, "Minimum reps for a set is 1.");
            num_reps_input.val("1");
            return;
        }
        if(!Number.isInteger(num_sets)) {
            add_alert(ALERT_TYPES.ERROR,"Exercise duration must be a number.");
            num_sets_input.value("3");
            return;
        }
        if (num_sets <= 0) {
            add_alert(ALERT_TYPES.ERROR, "You must have at least 1 set.");
            num_sets_input.value("1");
            return;
        }

        cardio_exercise_name_input.val("");
        cardio_exercise_duration_input.val("30");
        num_reps_input.val("10");
        num_sets_input.val("3");

        // Create a new exercise object
        const new_exercise = new Exercise({
            id: Object.values(current_exercise_routine).length,
            exercise: exercise_name,
            duration: exercise_duration,
            sets: num_sets,
            reps: num_reps,
        });

        // Add the exercise to the routine array
        current_exercise_routine[new_exercise.id] = new_exercise;
        render_tables();
    }

    add_cardio_btn.click(function(){
        add_exercise(cardio_exercise_name_input.val());
        cardio_exercise_name_input.val("");
    });
    add_strength_btn.click(function(){
        add_exercise(strength_exercise_name_input.val());
        strength_exercise_name_input.val("");
    });

    /*
    * Updates the tables and hidden input for the current routine.
     */
    function render_tables(){
        $("#routine-table tbody tr").remove();
        $("#mobile-table .mobile-table-card").remove();
        exercise_routine_input.val(JSON.stringify(Object.values(current_exercise_routine)));

        Object.values(current_exercise_routine).forEach(exercise => {
            $("#routine-table tbody").append(exercise.table_element());
            $("#mobile-table").append(exercise.mobile_table_element());
        });
        update_routine_display();
    }


    let exercise_routine_input = $("#exercise-routine");
    let current_exercise_routine = {};
    if(exercise_routine_input.val() !== "null") {
        JSON.parse(exercise_routine_input.val()).forEach((exercise, index) => {
                exercise = new Exercise({id: index, ...exercise});
                current_exercise_routine[exercise.id] = exercise;
            }
        );
    }
    render_tables();


    // Function to get the element ID to look up related exercise with.
    const get_element_id = (element) => element.id.slice(element.id.indexOf("_")+1);

    /*
    * Moves the selected exercise up.
    * element: The HTML element representing an exercise to move up.
     */
    function move_exercise_up(element){
        const exercise_id = get_element_id(element);
        const current_order = Object.values(current_exercise_routine);
        // No need to do anything if this is the first element
        if(exercise_id === current_order[0].id)
            return;

        let index = 0;
        current_exercise_routine = {};
        for(let exercise of current_order){
            if(exercise.id === exercise_id) {
                let temp_current_order = Object.values(current_exercise_routine);
                let before_exercise = temp_current_order[index - 1];
                // Move the matching element up.
                exercise.set_exercise_id(index -1)
                current_exercise_routine[exercise.id] = exercise;
                // Move the element from above down one.
                before_exercise.set_exercise_id(index)
                current_exercise_routine[before_exercise.id] = before_exercise;
            }
            else {
                exercise.set_exercise_id(index)
                current_exercise_routine[exercise.id] = exercise;
            }
            index ++;
        }
        render_tables();
    }

    $("#routine-table").on("click",".routine-actions .move-exercise-up", function(element){
        move_exercise_up(element.currentTarget.closest("tr"));
    });
    $("#mobile-table").on("click",".routine-actions .move-exercise-up", function(element){
        move_exercise_up(element.currentTarget.closest("div.mobile-table-card"));
    });

    /*
    * Moves the exercise element down in the list.
    * element: The html element to find a matching exercise pair for.
     */
    function move_exercise_down(element){
        const exercise_id = get_element_id(element);
        const current_order = Object.values(current_exercise_routine);

        let matching_element = undefined;
        let index = 0;
        current_exercise_routine = {};
        for(let exercise of current_order){
            if(exercise.id === exercise_id) {
                matching_element = exercise;
                continue;
            }
            exercise.set_exercise_id(index);
            current_exercise_routine[exercise.id] = exercise;
            index ++;

            // Put the matching exercise below the current exercise.
            if (matching_element !== undefined) {
                matching_element.set_exercise_id(index);
                current_exercise_routine[matching_element.id] = matching_element;
                matching_element = undefined;
                index ++;
            }
        }

        // If the element selected was the bottom most, we need to re-add it.
        if(matching_element !== undefined) {
            matching_element.set_exercise_id(index);
            current_exercise_routine[matching_element.id] = matching_element;
        }
        render_tables();
    }

    $("#routine-table").on("click", ".routine-actions .move-exercise-down", function(element){
        move_exercise_down(element.currentTarget.closest("tr"));
    });
    $("#mobile-table").on("click",".routine-actions .move-exercise-down", function(element){
        move_exercise_down(element.currentTarget.closest("div.mobile-table-card"));
    });

    /*
    * Removes an exercise element from the table.
    * element: The HTML element to find a matching exercise object with.
     */
    function delete_exercise(element){
        const exercise_id = get_element_id(element);
        delete current_exercise_routine[exercise_id];
        render_tables();
    }

    $("#routine-table").on("click", ".routine-actions .remove-exercise", function(element){
        delete_exercise(element.currentTarget.closest("tr"))
    });
    $("#mobile-table").on("click",".routine-actions .remove-exercise", function(element){
        delete_exercise(element.currentTarget.closest("div.mobile-table-card"));
    });

});