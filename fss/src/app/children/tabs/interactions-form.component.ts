import { Component, OnChanges, OnInit, Input, Output, EventEmitter, SimpleChanges } from '@angular/core';
import { FileUploader, FileItem, FileUploaderOptions, FileLikeObject } from 'ng2-file-upload';
import { DatePipe } from '@angular/common';
import { MatSnackBar } from '@angular/material';

import { Child } from '../../child';
import { Interaction } from '../../interaction';
import { RestService } from '../../rest.service';

@Component({
	selector: 'interactions-form',
	templateUrl: './interactions-form.component.html',
	styleUrls: ['./interactions-form.component.scss']
})
export class InteractionsFormComponent implements OnInit, OnChanges {
    @Input() child_id: number;
    @Input() interaction: Interaction;
    private fileuploader: FileUploader;
    // Send the string "deleted" or "hidden"
    @Output() notifyDeletedOrHidden = new EventEmitter<string>();
    private child: Child;
    private interaction_coordinators: String[];
    private interaction_types: String[];
    private uploaded_files: String[];

    constructor(
        private restService: RestService,
        private datePipe: DatePipe,
        public snackBar: MatSnackBar
    ) { }

    ngOnInit(): void {
        this.fileuploader = new FileUploader({
            url: this.restService.getPhotoUploadUrl(),
            itemAlias: 'interactions',
            //allowedMimeType: this.allowed_mime_type,
            additionalParameter: { interaction_id: this.interaction.id }
        });
        this.fileuploader.onAfterAddingAll = (files: FileItem[]) => {
            this.fileuploader.uploadAll();
        }
        this.fileuploader.onCompleteItem = (file: FileItem, message: string, status: number) => {
            let snackbar_message: string;
            if (status != 201) {
                snackbar_message = "Error uploading file!";
            } else {
                snackbar_message = "File uploaded!";
            }
            this.snackBar.open(snackbar_message, null, {
                duration: 2000,
            });
            //this.fileInput.nativeElement.value = '';
            this.ngOnChanges(null);
        }

        this.getChild();
        this.getInteractionCoordinators();
        this.getInteractionTypes();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges(null));
    }
    ngOnChanges(changes: SimpleChanges): void {
        this.getChild();
        this.getUploadedFiles();
    }
    getChild(): void {
        this.restService.getChild(this.child_id).then(child => this.child = child);
    }
    getUploadedFiles(): void {
        this.restService.getInteractionFiles(this.interaction.id).then(files => this.uploaded_files = files['filenames']);
    }
    getInteractionCoordinators(): void {
        this.restService.getEnum('fss_interaction_coordinator').then(coordinators => this.interaction_coordinators = coordinators);
    }
    getInteractionTypes(): void {
        this.restService.getEnum('fss_interaction_type').then(types => this.interaction_types = types);
    }
    saveInteraction(): void {
        this.interaction.interaction_date = this.restService.getStringFromDate(this.interaction.interaction_date_object);
        this.restService.updateInteraction(this.interaction);
    }
    deleteInteraction(): void {
        if (confirm("Are you sure you want to delete this interaction?")) {
            this.restService.deleteInteraction(this.interaction.id);
            this.interaction = null;
            this.notifyDeletedOrHidden.emit("deleted");
        }
    }
    deleteFile(filename: String): void {
        console.log("Create this!");
    }
    hideForm(): void {
        this.notifyDeletedOrHidden.emit("hidden");
    }
    setDate(date): void {
        this.interaction.interaction_date = this.datePipe.transform(date, 'yyyy-MM-dd');
    }
    showDetails(): boolean {
        let t = this.interaction.interaction_type;
        return t == 'Consultation SOAR Village' || t == 'Consultation FSS Centre' || t == 'Home visit';
    }

    // Dirty hack to style <input type=file> with angular meterial. Also can use label and style that, but that doesn't work well with angular meterial
    public openFileSelect(): void {
        document.getElementById("interaction-file-select").click();
    }
}
