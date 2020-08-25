% rebase("osnova.tpl")
    <form action="/delnice/">
    <!--<div class="title notification is-success has-text-centered">
        Analiza delnic
    </div>-->
        <div class="container">
            <div class="notification">
                <div class="columns">
                    <div class="column mx-4 my-4 px-0 py-0">
    
                        <h1 class="mb-3 has-text-weight-bold is-size-5"> Delnica: </h1>
                        
                        <div class="field mb-5 control select is-success select is-rounded">
                            <select name="Company" id="podjetje">
                            % for x in seznam_firm:
                                <option value="{{x}}">{{x}}</option>
                            %end
                            </select>
                        </div>

                        <h1 class="has-text-weight-bold is-size-5 mb-3">Število let:</h1>

                        <div class="field mb-5 control select is-success select is-rounded">
                            <select name="Years" id="leta">
                                % for x in range(1,11):
                                <option value="{{x}}">{{x}}</option>
                                %end
                            </select>
                        </div>

                        <ul>
                            <li class="mb-1"> <input type="checkbox" name="P/E" value="P/E"> 
                                <label for="prodaja"> Cena/dobiček na delnico</label><br> </li>
                            <li class="mb-1"> <input type="checkbox" name="P/OCF" value="P/OCF">
                                <label for="net"> Cena/operativni denarni tok</label><br> </li>
                            <li class="mb-1"> <input type="checkbox" name="P/B" value="P/B">
                                <label for="operativni"> Cena/knjigovodska vrednost delnice</label><br> </li>
                            <li class="mb-5"> <input type="checkbox" name="Dividenda" value="Dividenda">
                                <label for="net"> Dividenda</label><br> </li>
                        </ul>

                        <h1 class="has-text-weight-bold is-size-5 mb-3">Povprečna letna rast:</h1>

                        <ul>
                            <li class="mb-1"> <input type="checkbox" name="prodaja" value="Revenue"> 
                                <label for="prodaja"> Prodaje</label><br> </li>
                            <li class="mb-1"> <input type="checkbox" name="operativni" value="Operating Income">
                                <label for="operativni"> Operativnega dobička</label><br> </li>
                            <li class="mb-1"> <input type="checkbox" name="net" value="Net Income">
                                <label for="net"> Dobička po davku</label><br> </li>
                            <li class="mb-5"> <input type="checkbox" name="OCF" value="Operating Cash Flow">
                                <label for="net"> Operativnega denarnega toka</label><br> </li>
                        </ul>
                        %if not seznam_firm==[]:
                        <input class="button is-success is-rounded" type="submit" value="ZAŽENI">
                        %end

                    </div>
                    <div class="column mx-4 my-4 px-0 py-0 has-text-weight">

                        <h2 class="has-text-weight-bold is-size-6 mb-1">Priprava okolja:<h2>
                        <ol type="1">
                            <li class="mb-1"> Pojdite na spletno stran <a href="https://www.morningstar.com/">morningstar</a>.</li>
                            <li class="mb-1"> Poiščite podjetje, ki ga želite analizirati.</li>
                            <li class="mb-1"> Izberite Key ratios, ki se nahajajo desno od grafa cene delnice,
                             in jih naložite v enako mapo, v kateri se nahaja ta program.</li>
                        </ol>

                        <h2 class="has-text-weight-bold is-size-6 mb-1 mt-3">Uporaba programa:<h2>
                        <ol type="1">
                            <li class="mb-1"> Pod možnostjo IZBERITE PODJETJE izberite željeno podjetje.</li>
                            <li class="mb-1"> Nato izberite obdobje za katerega želite, da se izračunata koeficienta cena/dobiček na delnico
                             ter cena/operativni denarni tok <b>(v letih)</b>.<br> <b>Opomba:</b> cena/knjigovodsta vrednost delnice in dividenda
                             se izračunata za zadnje znane podatke. Povprečna letna rast pa je povprečje letne rasti v zadnjih desetih letih.</li> 
                            <li class="mb-1"> Podatke, ki jih želite za analizo označite s kljukico.</li>
                            <li class="mb-1"> Pritisnite ZAŽENI.</li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
    </form>
