#!/bin/sh

Remote=$1
Tag=$2
Config=config/${Tag}.json

if [ "${Tag}" = "" ] || [ "${Remote}" = "" ]
then
  echo "Need remote host and config tag." >&2
  exit 10
fi


ModelFile=$(jq -r .model_file <"${Config}")
ParamsFile=$(jq -r .model_params <"${Config}")
TrainFile=$(jq -r .train_tf <"${Config}")
ValFile=$(jq -r .val_tf <"${Config}")

ssh "${Remote}" mkdir -p run
rsync -vaz text-train.py "${Remote}:run/train.py"
rsync -vaz "${ModelFile}" "${Remote}:run/model.h5"
rsync -vaz "${ParamsFile}" "${Remote}:run/params.json"
rsync -va --inplace --progress "${TrainFile}" "${Remote}:run/train.tfrecords"
rsync -va --inplace --progress "${ValFile}" "${Remote}:run/val.tfrecords"

ssh "${Remote}" 'source venv/bin/activate; cd run; ./train.py'
