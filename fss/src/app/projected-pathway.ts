import * as moment from 'moment';

export class ProjectedPathway {
	id: number;
	child_id: number;
	pathway_completion_date: string;
	pathway_details: string;
	pathway_short_description: string;
	pathway_step_number: number;
	pathway_completion_date_object: moment.Moment;
	pathway_is_active: boolean;
}
