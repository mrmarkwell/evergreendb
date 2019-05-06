import { Component, OnChanges, OnInit, Input } from '@angular/core';
import { FileUploader, FileItem, FileUploaderOptions, FileLikeObject } from 'ng2-file-upload';
import { MatSnackBar } from '@angular/material';

import { Child } from '../../child';
import { RestService } from '../../rest.service';

@Component({
    selector: 'medical-info-tab',
    styleUrls: ['./medical-info-tab.component.scss'],
    templateUrl: './medical-info-tab.component.html'
})
export class MedicalTabComponent implements OnInit, OnChanges {
    child: Child;
    private fileuploader: FileUploader;
    private conditions: String[];
    private uploaded_files: String[];
    constructor(
        public snackBar: MatSnackBar,
        private restService: RestService
    ) {}
    ngOnInit(): void {
        this.getChild();
        this.getMedicalConditions();
        this.restService.changeEmitter.subscribe(() => this.ngOnChanges())

        this.fileuploader = new FileUploader({
            url: this.restService.getPhotoUploadUrl(),
            itemAlias: 'medical',
            additionalParameter: { child_id: this.child_id }
        });
        this.fileuploader.onAfterAddingAll = (files: FileItem[]) => {
            this.fileuploader.options.additionalParameter.child_id = this.child_id;
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
            this.ngOnChanges();
        }
    }
    ngOnChanges(): void {
        this.getChild();
        this.getUploadedFiles();
    }
    getChild(): void {
        this.restService.getChild(this.child_id).then(child => {
            this.child = child;
        });
    }
    getMedicalConditions(): void {
        this.restService.getEnum('fss_medical_condition').then(conditions => this.conditions = conditions)
    }
    getUploadedFiles(): void {
        this.restService.getMedicalFiles(this.child_id).then(files => this.uploaded_files = files['filenames']);
    }
    deleteFile(filename: String): void {
        let index: number = this.uploaded_files.indexOf(filename, 0);
        if (index > -1) {
           this.uploaded_files.splice(index, 1);
        }
        if (confirm("Are you sure you want to delete file " + filename + "?")) {
        this.restService.deleteMedicalFile(this.child_id, this.uploaded_files);
        }
    }
    // Dirty hack to style <input type=file> with angular meterial. Also can use label and style that, but that doesn't work well with angular meterial
    public openFileSelect(): void {
        document.getElementById("medical-file-select").click();
    }
    @Input() child_id: number;
}
