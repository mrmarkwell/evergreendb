import * as moment from 'moment';
export class Child {
	constructor(jsondata){
		for (let attr in jsondata) {
			this[attr] = jsondata[attr];
		}
	}

	getAge(): number {
		if (this.birth_date == null || this.birth_date.length == 0) return null;
		return moment().diff(this.birth_date, 'years');
	}

	equals(c2: Child) : boolean {
		return this.id == c2.id
			&& this.birth_date == c2.birth_date
			&& this.birth_history == c2.birth_history
			&& this.child_chinese_name == c2.child_chinese_name
			&& this.child_english_name == c2.child_english_name
			&& this.child_pinyin_name == c2.child_pinyin_name
			&& this.family_dynamics == c2.family_dynamics
			&& this.further_diagnosis == c2.further_diagnosis
			&& this.gender == c2.gender
			&& this.medical_history == c2.medical_history
			&& this.nickname == c2.nickname
			&& this.primary_diagnosis == c2.primary_diagnosis
			&& this.primary_diagnosis_note == c2.primary_diagnosis_note
			&& this.reason_for_referral == c2.reason_for_referral
			&& this.referred_by == c2.referred_by
			&& this.secondary_diagnosis == c2.secondary_diagnosis
			&& this.secondary_diagnosis_note == c2.secondary_diagnosis_note
			&& this.status == c2.status
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
	birth_date_object: moment.Moment;
}
