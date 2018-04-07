import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { RestService } from '../rest.service'
//import 'rxjs/add/operator/fromPromise';
import { fromPromise } from 'rxjs/observable/fromPromise'

@Injectable()
export class AdminAuthGuard implements CanActivate {
    constructor(
        private restService: RestService
    ) { }

    canActivate(
        route: ActivatedRouteSnapshot,
        state: RouterStateSnapshot
    ): Observable<boolean> {
        return fromPromise(this.restService.checkAdminLogin());
    }
}