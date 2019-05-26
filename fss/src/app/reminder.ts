import { Interaction } from 'app/interaction';
import { ProjectedPathway } from 'app/projected-pathway';
import * as moment from 'moment';

export class Reminder {
    static fromInteraction(interaction) {
        return new this(
            interaction.child_id,
            interaction.interaction_date,
            interaction.interaction_type,
            interaction.interaction_notes
        )
    }

    static fromProjectedPathway(projected_pathway) {
        return new this(
            projected_pathway.child_id,
            projected_pathway.pathway_completion_date,
            "Projected Pathway",
            projected_pathway.pathway_short_description
        )
    }

    constructor(
        public child_id: number,
        public date: string,
        public type: string,
        public notes: string,
    ) {}

    date_object: moment.Moment;
    child_chinese_name: string;
    child_pinyin_name: string;
}
