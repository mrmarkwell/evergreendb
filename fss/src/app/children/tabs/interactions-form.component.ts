import { Component, OnChanges, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { DatePipe } from '@angular/common';

import { Child } from '../../child';
import { Interaction } from '../../interaction';
import { RestService } from '../../rest.service';

@Component({
	selector: 'interactions-form',
	templateUrl: './interactions-form.component.html',
	styleUrls: ['./interactions-form.component.css']
})
export class InteractionsFormComponent implements OnInit, OnChanges {
	@Input() child_id: number;
	@Input() interaction: Interaction;
	@Output() notifyDeleted = new EventEmitter<null>();
	private child: Child;
	private interaction_coordinators: String[];
	private interaction_types: String[];
	constructor(
		private restService: RestService,
		private datePipe: DatePipe
	) {}

	ngOnInit(): void {
		this.getChild();
		this.getInteractionCoordinators();
		this.getInteractionTypes();
		this.restService.changeEmitter.subscribe(() => this.ngOnChanges());
	}
	ngOnChanges(): void {
		this.getChild();
	}
	getChild(): void {
		this.restService.getChild(this.child_id).then(child => this.child = child);
	}
	getInteractionCoordinators(): void {
		this.restService.getEnum('fss_interaction_coordinator').then(coordinators => this.interaction_coordinators = coordinators);
	}
	getInteractionTypes(): void {
		this.restService.getEnum('fss_interaction_type').then(types => this.interaction_types = types);
	}
	saveInteraction(): void {
		this.restService.updateInteraction(this.interaction).then(interaction => this.interaction = interaction);
		this.restService.updateChild(this.child).then(child => this.child = child);
	}
	deleteInteraction(): void {
		if (confirm("Are you sure you want to delete this interaction?")) {
			this.restService.deleteInteraction(this.interaction.id);
			this.interaction = null;
			this.notifyDeleted.emit();
		}
	}
	hideForm(): void {
		this.interaction = null;
	}
	setDate(date): void {
		console.log(date);
		this.interaction.interaction_date = this.datePipe.transform(date, 'yyyy-MM-dd');
		console.log(this.interaction.interaction_date);
	}
	showDetails(): boolean {
		let t = this.interaction.interaction_type;
		return t == 'Consultation SOAR Village' || t == 'Consultation FSS Centre' || t == 'Home visit';
	}
}
