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
            // populate date object
            for (let reminder of reminders) {
                reminder.date_object = this.restService.getDateFromString(reminder.date)
            }
            this.allReminders = reminders;
        });
    }
}
