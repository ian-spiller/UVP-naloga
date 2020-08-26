% rebase("osnova.tpl")
    <h1 class="has-text-weight-bold is-size-3 has-text-centered mb-4">Rezultati</h1>
    <ul class="has-text-centered">
        <li class="has-text-weight-bold is-size-5">Kratica delniške družbe na NYSE: {{kratica}}</li>
        <li class="has-text-weight-bold is-size-6">Cena: {{cena}}$</li>
    </ul>
    <div class="columns my-6">
         <div class="column" style="border-color:hsl(141, 71%, 48%); border-style:solid; border-radius:30px 30px 30px 30px;">
         <h1 class="has-text-weight-bold is-size-5 has-text-centered mt-3 mb-4">Izračuni koeficientov:</h1>
         <ol class="ml-5 mb-4">
            % if not P_E=="Ni zahteve":
            <li class="my-3">
                <ul>
                    <li>
                     Povprečen koeficient cena/zaslužek zadnjih {{leta}} let: <b>{{price_earning}}</b> </li>
                    % if not brez_vrednosti_eps==0:
                    <li class="has-text-danger"> Število mankajočih podatkov: {{brez_vrednosti_eps}}</li>
                    %end
                    %if not negativne_vrednosti_eps==0:
                    <li class="has-text-danger"> Kolikokrat je bil zaslužek negativen: {{negativne_vrednosti_eps}}</li>
                    %end
                </ul>
            </li>
            %end
        
            % if not P_OCF=="Ni zahteve":
            <li class="my-3">
                <ul>
                    <li> 
                        Povprečen koeficient cena/operativni denarni tok zadnjih {{leta}} let: <b>{{price_OCF}}</b> </li>
                    %if not brez_vrednosti_OCF==0:
                    <li class="has-text-danger"> Število mankajočih podatkov: {{brez_vrednosti_OCF}}</li>
                    %end
                    %if not negativne_vrednosti_OCF==0:
                    <li class="has-text-danger"> Kolikokrat je bil operativni denarni tok negativen: {{negativne_vrednosti_OCF}}</li>
                    %end
                </ul>
            </li>
            %end

             % if not P_B=="Ni zahteve":
            <li class="my-3">
                <ul>
                    <li> Trenuten koeficient cena/knjigovodska vrednost delnice: <b>{{price_book}}</b> </li>
                    % if not problem_P_B=="":
                    <li class="has-text-danger"> Prišlo je do težave: {{problem_P_B}}</li>
                    %end
                </ul>
            </li>
            %end

            % if not Dividenda_1=="Ni zahteve":
            <li class="my-3">
                Trenutna stopnja dividende: <b>{{dividenda}}</b>%
            </li>
            %end
        </ol>
        </div>

        <div class="column is-1">
        </div>

        <div class="column" style="border-color:hsl(141, 71%, 48%); border-style:solid;border-radius:30px 30px 30px 30px;">
        <h1 class="has-text-weight-bold is-size-5 has-text-centered mt-3 mb-4">Izračuni rasti:</h1>
        <ol class="ml-5 mb-4">
            % if not rast_prodaja=="Ni zahteve":
            <li class="mt-3">
                <ul>
                    %if rast_prodaja=="Negativna vrednost":
                    <li class="has-text-danger">Če se pojavi ta vrstica, nismo uspeli izračunati rasti, saj so podatki negativni.</li>
                    %else:
                    <li> Povprečna letna rast prodaje v zadnjih destih letih: <b>{{rast_prodaja}}%</b> </li>
                    %end
                    % if not koliko_letna_rast_prodaja==10:
                    <li class="has-text-danger">Če se pojavi ta vrstica, nismo uspeli dobiti vseh podatkov zato
                    je podatek v prejšnji vrstici izračunan za: {{koliko_letna_rast_prodaja}} let</li>
                    % end
                </ul>
            </li>
            %end

             % if not rast_operating=="Ni zahteve":
            <li class="my-3">
                <ul>
                    %if rast_operating== "Negativna vrednost":
                    <li class="has-text-danger">Če se pojavi ta vrstica, nismo uspeli izračunati rasti, saj so podatki negativni.</li>
                    %else:
                    <li> Povprečna letna rast operativnega zasluška v zadnjih destih letih: <b>{{rast_operating}}%</b> </li>
                    %end
                    % if not koliko_letna_rast_operating==10:
                    <li class="has-text-danger"> Če se pojavi ta vrstica, nismo uspeli dobiti vseh podatkov zato
                    je podatek v prejšnji vrstici izračunan za: {{koliko_letna_rast_operating}} let</li>
                    %end
                </ul>
            </li>
            %end

            % if not rast_net=="Ni zahteve":
            <li class="my-3">
                <ul>
                    %if rast_net=="Negativna vrednost":
                    <li class="has-text-danger">Če se pojavi ta vrstica, nismo uspeli izračunati rasti, saj so podatki negativni.</li>
                    %else:
                    <li> Povprečna letna rast dobička v zadnjih destih letih: <b>{{rast_net}}%</b></li>
                    %end
                    % if not koliko_letna_rast_net==10:
                    <li class="has-text-danger"> Če se pojavi ta vrstica, nismo uspeli dobiti vseh podatkov zato
                    je podatek v prejšnji vrstici izračunan za: {{koliko_letna_rast_net}} let</li>
                    %end
                </ul>
            </li>
            %end

            % if not rast_OCF=="Ni zahteve":
            <li class="my-3">
                <ul>
                    %if rast_OCF=="Negativna vrednost":
                    <li class="has-text-danger">Če se pojavi ta vrstica, nismo uspeli izračunati rasti, saj so podatki negativni.</li>
                    %else:
                    <li> Povprečna letna rast denarnega operativnega toka v zadnjih destih letih: <b>{{rast_OCF}}%</b></li>
                    %end
                    % if not koliko_letna_rast_OCF==10:
                    <li class="has-text-danger"> Če se pojavi ta vrstica, nismo uspeli dobiti vseh podatkov zato
                    je podatek v prejšnji vrstici izračunan za: {{koliko_letna_rast_OCF}} let</li>
                    %end
                </ul>
            </li>
            %end

        </ol>
        </div>
    </div>
  