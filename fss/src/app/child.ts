export class Child {
	constructor(jsondata){
		for (let attr in jsondata) {
			this[attr] = jsondata[attr];
		}
	}

	getAge(): number {
		let bdate_split = this.birth_date.split('-');
		let today = new Date();
		let no_bday_yet = Number( bdate_split[1] + bdate_split[2] ) > ( (today.getMonth()+1)*100 + today.getDate() ); // Not elegant, I know...
		return today.getFullYear() - Number(bdate_split[0]) + (no_bday_yet ? -1 : 0);
	}

	id: number;
	birth_date: string;
	birth_history: string;
	child_chinese_name: string;
	child_english_name: string;
	child_pinyin_name: string;
	developmental_notes: string;
	developmental_recommendations: string;
	feeding_recommendations: string;
	fine_motor_notes: string;
	fine_motor_recommendations: string;
	further_diagnosis: string;
	gender: string;
	gross_motor_notes: string;
	gross_motor_recommendations: string;
	head_control: boolean;
	medical_history: string;
	milk_feeding: boolean;
	nickname: string;
	ot_notes: string;
	ot_recommendations: string;
	physical_recommendations: string;
	primary_diagnosis: string;
	primary_diagnosis_note: string;
	reason_for_referral: string;
	referred_by: string;
	rolling: boolean;
	secondary_diagnosis: string;
	secondary_diagnosis_note: string;
	self_feeding: boolean;
	sensory_notes: string;
	sensory_recommendations: string;
	sitting: boolean;
	solid_feeding: boolean;
	speech_notes: string;
	speech_recommendations: string;
	standing: boolean;
	status: string;
	texture_preferences: string;
	walking: boolean;
	weakness_notes: string;
	weakness_recommendations: string;
	birth_date_object: Date;
}
