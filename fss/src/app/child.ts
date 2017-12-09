export class Child {
	constructor(jsondata){
		for (let attr in jsondata) {
			this[attr] = jsondata[attr];
		}
	}

	getAge(): number {
		if (this.birth_date == null || this.birth_date.length == 0) return null;
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
	family_dynamics: string;
	further_diagnosis: string;
	gender: string;
	medical_history: string;
	nickname: string;
	primary_diagnosis: string;
	primary_diagnosis_note: string;
	reason_for_referral: string;
	referred_by: string;
	secondary_diagnosis: string;
	secondary_diagnosis_note: string;
	status: string;
	birth_date_object: Date;
}
