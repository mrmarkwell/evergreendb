import * as moment from 'moment';


import { Component, OnInit, OnChanges, EventEmitter, Output, Input } from '@angular/core';
import { RestService } from '../rest.service';
import { Reminder } from 'app/reminder';

@Component({
    selector: 'reminder-list',
    templateUrl: 'reminder-list.component.html',
    styleUrls: ['reminder-list.component.scss']
})

export class ReminderList implements OnInit, OnChanges {
    allReminders: Reminder[];
    filteredReminders: Reminder[];

    ngOnInit(): void {
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())
        this.getReminders();
    }

    ngOnChanges(): void {
        this.getReminders();
    }

    constructor(private restService: RestService) { }

    getReminders(): void {
        this.restService.getAllReminders().then(reminders => {
            reminders.forEach(reminder => {
                this.restService.getChild(reminder.child_id).then(child => {
                    reminder.child_chinese_name = child.child_chinese_name;
                    reminder.child_pinyin_name = child.child_pinyin_name;
                });
            });
            
            // populate date object
            for (let reminder of reminders) {
                reminder.date_object = this.restService.getDateFromString(reminder.date)
            }
            // sort the list by date object
            this.allReminders = reminders.sort((n1,n2) => {
                if (n1.date_object < n2.date_object) {
                    return -1;
                }
                if (n1.date_object > n2.date_object) {
                    return 1;
                }
                return 0;
            });

            let d = moment();
            this.filteredReminders = this.allReminders.filter(reminder => reminder.date_object > d)
        });
    }
}
