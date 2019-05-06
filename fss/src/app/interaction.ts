import * as moment from 'moment';

export class Interaction {
	constructor(jsondata){
		for (let attr in jsondata) {
			this[attr] = jsondata[attr];
		}
	}

	equals(i2: Interaction): boolean {
		return this.id == i2.id
			&& this.child_id == i2.child_id
			&& this.current_concerns == i2.current_concerns
			&& this.dev_history == i2.dev_history
			&& this.dev_since_last_visit == i2.dev_since_last_visit
			&& this.follow_up == i2.follow_up
			&& this.interaction_coordinator == i2.interaction_coordinator
			&& this.interaction_date == i2.interaction_date
			&& this.interaction_notes == i2.interaction_notes
			&& this.interaction_type == i2.interaction_type
			&& this.is_initial_interaction == i2.is_initial_interaction
			&& this.people_present == i2.people_present
			&& this.milk_feeding == i2.milk_feeding
			&& this.solid_feeding == i2.solid_feeding
			&& this.self_feeding == i2.self_feeding
			&& this.texture_preferences == i2.texture_preferences
			&& this.feeding_recommendations == i2.feeding_recommendations
			&& this.developmental_notes == i2.developmental_notes
			&& this.developmental_recommendations == i2.developmental_recommendations
			&& this.ot_notes == i2.ot_notes
			&& this.ot_recommendations == i2.ot_recommendations
			&& this.sensory_notes == i2.sensory_notes
			&& this.sensory_recommendations == i2.sensory_recommendations
			&& this.speech_notes == i2.speech_notes
			&& this.speech_recommendations == i2.speech_recommendations
			&& this.head_control == i2.head_control
			&& this.rolling == i2.rolling
			&& this.sitting == i2.sitting
			&& this.standing == i2.standing
			&& this.walking == i2.walking
			&& this.weakness_notes == i2.weakness_notes
			&& this.weakness_recommendations == i2.weakness_recommendations
			&& this.physical_recommendations == i2.physical_recommendations
			&& this.gross_motor_notes == i2.gross_motor_notes
			&& this.gross_motor_recommendations == i2.gross_motor_recommendations
			&& this.fine_motor_notes == i2.fine_motor_notes;
	}

	id: number;
	child_id: number;
	current_concerns: string;
	dev_history: string;
	dev_since_last_visit: string;
	follow_up: string;
	interaction_coordinator: string;
	interaction_date: string;
	interaction_notes: string;
	interaction_type: string;
	is_initial_interaction: boolean;
	people_present: string;
	interaction_date_object: moment.Moment;

	milk_feeding: boolean;
	solid_feeding: boolean;
	self_feeding: boolean;
	texture_preferences: string;
	feeding_recommendations: string;
	developmental_notes: string;
	developmental_recommendations: string;
	ot_notes: string;
	ot_recommendations: string;
	sensory_notes: string;
	sensory_recommendations: string;
	speech_notes: string;
	speech_recommendations: string;
	head_control: boolean;
	rolling: boolean;
	sitting: boolean;
	standing: boolean;
	walking: boolean;
	weakness_notes: string;
	weakness_recommendations: string;
	physical_recommendations: string;
	gross_motor_notes: string;
	gross_motor_recommendations: string;
	fine_motor_notes: string;
	fine_motor_recommendations: string;

	// This is not coming from the backend
	has_attachments: boolean;
}
