class Exercise {
    constructor({ exercise, reps, sets, duration }) {
        this.exercise = exercise;
        this.reps = reps || 0;
        this.sets = sets || 0;
        this.duration = duration || 0;
    }

    table_element() {
        return `
            <tr>
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
            <div class="mobile-table-card">
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

    let exercise_routine_input = $("#exercise-routine");
    let current_exercise_routine = exercise_routine_input.val();
    if(current_exercise_routine === undefined || current_exercise_routine === null) {}
        current_exercise_routine = []
    // Todo: Else: Load in the routine


    const add_cardio_btn = $("#add-cardio-exercise");
    const cardio_exercise_name_input = $("#cardio-exercise");
    const cardio_exercise_duration_input = $("#cardio-duration");
    function add_cardio_exercise() {
        const exercise_name = cardio_exercise_name_input.val();
        const exercise_duration = parseInt(cardio_exercise_duration_input.val());
        if (exercise_name === "") {
            console.error("No name provided for exercise.");
            return;
        }
        if (!Number.isInteger(exercise_duration)) {
            console.error("Exercise duration must be a number.");
            cardio_exercise_duration_input.val("30");
            return;
        }
        if (exercise_duration < 5) {
            console.error("Exercise duration must be at least 5 seconds.");
            return;
        }

        cardio_exercise_name_input.val("");
        cardio_exercise_duration_input.val("30");

        // Create a new exercise object
        const new_exercise = new Exercise({ exercise: exercise_name, duration: exercise_duration });

        // Add the exercise to the routine array
        current_exercise_routine.push(new_exercise);
        exercise_routine_input.val(JSON.stringify(current_exercise_routine));

        // Append new elements to the table and mobile table
        $("#routine-table").append(new_exercise.table_element());
        $("#mobile-table").append(new_exercise.mobile_table_element());
        update_routine_display();
    }


    add_cardio_btn.click(add_cardio_exercise)

});