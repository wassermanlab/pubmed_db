<strong>README</strong>
=====
Instructions on how to update the PubMedDB annually.


Table of Contents
-----
1. [Conda](#conda-environment)
2. [Download PubMed Baseline](#baseline)
3. [XML to JSON](#xml-to-json)
4. [Use MongoDB](#get-mongodb-database)

<br>

Conda Environment
-----
All packages are provided within the YML environment file. A conda environment named `pubmeddb` can be created using the following command.
```bash
conda env create -f ./pubmeddb.yml
```
<br>
<br>

JSON Fields
-----
<table>
<tr>
<th>
PubMedID Collection
</th>
<th>
Gene Collection
</th>
</tr>

<tr>
<td>
<pre>
{
    	"PMID":"XX",
    	"ArticleTitle": "xx",
    	"Abstract":{
	        	"Text": "...",
	        	"Words":{
	            	"Word1":{
		                	"Stems": [xx , xx, xx],
		                	"Count": 1
           		        },
			        "Word2":{ 
		                	"Stems": [xx , xx, xx],
		                	"Count": 1
                        }
		            }
                },
        "Country": "XX",
	    "MeshHeading":{
		    "MeshIdentifier (Ex. D000818)":{
			    "DescriptorName": "XX",
			    "QualifierName":{}
		}
	}	
}
</pre>
</td>

<td>
<pre>
{
    	"GeneID": XX,
	“Name”: XX
    	"TaxonomyID": XX,
    	"PubMedID": [xx , xx, xx]
}
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
</pre>
</td>

</table>




Baseline
-----
Please use the <strong>DATA TRANSFER node</strong> of Sockeye to download the PubMed baseline (https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/) and gene2pubmed (https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz).
```bash
ssh <cwl>@dtn.sockeye.arc.ubc.ca
```
<br>

Run download script:
```bash
bash ./utils/dl_pubmeddata.sh
```
<br>
<br>

XML to JSON
-----
Please edit the `PBS -M` with your email address in `pubmed_submit.sh`.
```bash
##PBS -M <email>
```
<br>
Run the following code in the <strong>COMPUTE node</strong> and submit script as a job from a tempory/scratch directory (currently project directory is only readable by the compute nodes).

```bash
cd <SCRATCH DIR>
qsub /project/st-wasserww-1/PubMed_DB/pubmed_submit.sh
```
<br>
<br>

Get MongoDB Database
-----







