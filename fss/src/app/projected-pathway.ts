 import * as moment from 'moment';

export class ProjectedPathway {
  constructor(jsondata){
    for (let attr in jsondata) {
      this[attr] = jsondata[attr];
    }
  }

	equals(pp2: ProjectedPathway) : boolean {
		return this.id == pp2.id
			&& this.child_id == pp2.child_id
			&& this.pathway_completion_date == pp2.pathway_completion_date
			&& this.pathway_details == pp2.pathway_details
			&& this.pathway_short_description == pp2.pathway_short_description
			&& this.pathway_step_number == pp2.pathway_step_number
			&& this.pathway_is_active == pp2.pathway_is_active;
	}

	id: number;
	child_id: number;
	pathway_completion_date: string;
	pathway_details: string;
	pathway_short_description: string;
	pathway_step_number: number;
	pathway_completion_date_object: moment.Moment;
	pathway_is_active: boolean;
}
