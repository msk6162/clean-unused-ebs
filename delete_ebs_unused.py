import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')

def lambda_handler(event, context):
    deletedVolumes=[]
    for vol in ec2.volumes.all():
        if vol.state == 'available':
            if vol.tags is None:
                vid = vol.id
                v = ec2.Volume(vol.id)
                v.delete()
                deletedVolumes.append({'VolumeId': vol.id,'Status':'Delete Initiated'})
                print('Deleted ' + vid)
            else:
                Delete = True
                for tag in vol.tags:
                    Key = tag['Key']
                    if Key == 'DND':
                        Delete = False
                if Delete is True:
                    vid = vol.id
                    v = ec2.Volume(vol.id)
                    v.delete()
                    deletedVolumes.append({'VolumeId': vol.id,'Status':'Delete Initiated'})
                    print('Deleted ' + vid)
                    
    if not deletedVolumes:
        deletedVolumes.append({'VolumeId':None,'Status':None})
        
    return deletedVolumes
