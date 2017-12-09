import { Interaction } from 'app/interaction';

export class Reminder {
    constructor(interaction){
		this.interaction = interaction
    }
    
    interaction: Interaction;
    child_chinese_name: string;
    child_pinyin_name: string;
}