import * as moment from 'moment';

export class Interaction {
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
