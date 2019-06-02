import * as moment from 'moment';

export class Reminder {

    constructor(
        public child_id: number,
        public child_pinyin_name: string,
        public child_chinese_name: string,
        public child_nickname: string,
        public date: string,
        public type: string,
        public notes: string,
    ) {}

    date_object: moment.Moment;
}
