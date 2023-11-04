def generate_empty_files(dry_run=False):
    '''Generate empty files in stories folder.

    generates empty files named story_i-x-y-.md where i, x and y are integers.
    x and y start from 1193 and ending at 2899 with a step of 30.

    i is just an iteration number starting from 38. The i should be printed with 0 leading zeroes,
    i.e. the first one should be 030.

    if dry_run is True, then the files are not created. Instead, the name of to be create
    file is printed out.
    '''

    story_id = 38
    for i in range(1193, 2899, 30):
        story_file_name = 'stories/story_{:03d}-{}-{}.md'.format(story_id, i, i+29)
        prompt_file_name = 'prompts/story_{:03d}-{}-{}_prompt.md'.format(story_id, i, i+29)
        story_id += 1
        if dry_run:
            print(story_file_name)
            print(prompt_file_name)
        else:
            with open(story_file_name, 'w') as f:
                pass
            with open(prompt_file_name, 'w') as f:
                pass

if __name__ == '__main__':
    generate_empty_files(dry_run=False)